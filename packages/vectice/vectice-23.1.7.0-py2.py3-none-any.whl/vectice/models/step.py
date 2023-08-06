from __future__ import annotations

import logging
import pickle  # nosec
from io import IOBase
from typing import TYPE_CHECKING, Any

from PIL.Image import Image

import vectice
from vectice.api.http_error_handlers import VecticeException
from vectice.api.json.iteration import (
    IterationStatus,
    IterationStepArtifact,
    IterationStepArtifactInput,
    IterationStepArtifactType,
)
from vectice.api.json.model_version import ModelVersionOutput
from vectice.api.json.step import StepType
from vectice.models.attachment_container import AttachmentContainer
from vectice.models.resource.base import Resource
from vectice.models.resource.metadata import DatasetType
from vectice.utils.automatic_link_utils import (
    existing_dataset_logger,
    existing_model_logger,
    link_assets_to_step,
    link_dataset_to_step,
    wrapper_to_dataset,
)
from vectice.utils.common_utils import _check_image_path, _check_read_only, _get_image_variables
from vectice.utils.deprecation import deprecate

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.models import Iteration, Phase, Project, Workspace
    from vectice.models.dataset import Dataset
    from vectice.models.datasource.datawrapper.data_wrapper import DataWrapper
    from vectice.models.model import Model
    from vectice.models.step_dataset import StepDataset
    from vectice.models.step_number import StepNumber
    from vectice.models.step_string import StepString

_logger = logging.getLogger(__name__)

MISSING_DATASOURCE_ERROR_MESSAGE = "Cannot create modeling dataset. Missing %s data source."


class Step:
    """Model a Vectice step.

    Steps define the logical sequence of steps required to complete
    the phase along with their expected outcomes.

    Steps belong to an Iteration. The steps created under a Phase are
    Step Definitions that are then re-used in Iterations to iteratively
    complete the steps until a satisfactory result is obtained.

    ```tree
    phase 1
        step definition 1
        step definition 2
        step definition 3
    ```

    ```tree
    iteration 1 of phase 1
        step 1
        step 2
        step 3
    ```

    If steps are added to a phase after iterations have been created
    and completed, these steps won't appear in these iterations.

    NOTE: **Phases and Steps Definitions are created in the Vectice App,
    Iterations are created from the Vectice Python API.**

    To complete an iteration's step, you just need to assign a value to it.
    To access the step and assign a value, you can use the "slug" of the step:
    the slug is the name of the step, transformed to fit Python's naming rules,
    and prefixed with `step_`. For example, a step called "Clean Dataset" can
    be accessed with `my_iteration.step_clean_dataset`.

    Therefore, to complete a step:

    ```python
    my_clean_dataset = ...
    my_iteration.step_clean_dataset = my_clean_dataset
    ```

    Depending on the step, you can assign it a [`Model`][vectice.models.model.Model],
    a [`Dataset`][vectice.models.dataset.Dataset], code source, or attachments.
    """

    @deprecate(
        parameter="completed",
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The `completed` parameter is deprecated. "
        "Using `completed` will raise an error in v{fail_at}. "
        "The parameter will be removed in v{remove_at}.",
    )
    def __init__(
        self,
        id: int,
        iteration: Iteration,
        name: str,
        index: int,
        slug: str,
        description: str | None = None,
        completed: bool | None = None,
        artifacts: list[IterationStepArtifact] | None = None,
        step_type: StepType = StepType.Step,
        text: str | None = None,
    ):
        """Initialize a step.

        Vectice users shouldn't need to instantiate Steps manually,
        but here are the step parameters.

        Parameters:
            id: The step identifier.
            iteration: The iteration to which the step belongs.
            name: The name of the step.
            index: The index of the step.
            slug: The slug of the step.
            description: The description of the step.
            completed: Deprecated. Whether the step is completed.
            artifacts: The artifacts linked to the steps.
            step_type: The step type.
            text: The step text.
        """
        self._id = id
        self._iteration: Iteration = iteration
        self._name = name
        self._index = index
        self._description = description
        self._client = self._iteration._client
        self._completed = completed
        self._artifacts = artifacts or []
        self._slug = slug
        self._origin_dataset: Dataset | None = None
        self._clean_dataset: Dataset | None = None
        self._modeling_dataset: Dataset | None = None
        self._type: StepType = step_type
        self._text = text
        self._model: Model | None = None

        self._iteration_read_only = self._iteration._status in {IterationStatus.Completed, IterationStatus.Abandoned}
        if self._iteration_read_only:
            _logger.debug(f"Step {self.name}, iteration is {self._iteration._status.name} and is read-only!")

    def __repr__(self):
        return f"Step(name={self.name!r}, slug={self.slug!r}, id={self.id!r})"

    def __eq__(self, other: object):
        if not isinstance(other, Step):
            return NotImplemented
        return self.id == other.id

    def __iadd__(self, value):
        # TODO cyclic import
        from vectice.models.dataset import Dataset
        from vectice.models.model import Model

        if isinstance(value, Model):
            if self._type not in {StepType.StepModel, StepType.Step}:
                raise TypeError(f"A model can't be added to a step of type {self._type!r}.")
            model_artifact = self._register_model(value)
            self.artifacts.append(model_artifact)
            self._keep_artifacts_and_update_step(StepType.StepModel, value)
        elif isinstance(value, Dataset):
            if self._type not in {StepType.StepDataset, StepType.Step}:
                raise TypeError(f"A dataset can't be added to a step of type {self._type!r}.")
            dataset_artifact, _ = self._register_dataset(value)
            self.artifacts.append(dataset_artifact)
            self._keep_artifacts_and_update_step(StepType.StepDataset, value)
        else:
            raise TypeError(f"Expected Dataset or a Model, got {type(value)}")

    def _keep_artifacts_and_update_step(self, step_type: StepType, value) -> None:
        if self._type is StepType.Step:
            artifacts = self.iteration.step(self.name).artifacts

            def _get_artifact_id(artifact: IterationStepArtifact) -> int:
                if artifact.model_version_id:
                    return artifact.model_version_id
                if artifact.dataset_version_id:
                    return artifact.dataset_version_id
                if artifact.entity_file_id:
                    return artifact.entity_file_id
                raise ValueError("No artifact ID.")

            maintain_artifacts = [
                IterationStepArtifactInput(id=_get_artifact_id(artifact), type=artifact.type.value)
                for artifact in artifacts
            ]
            self._client.update_iteration_step_artifact(self.id, step_type, artifacts=maintain_artifacts)
            self._warn_step_change(value)

    def _refresh_step(self) -> Step:
        step = self._iteration.step(self.name)
        setattr(self._iteration, step.slug, step)
        return step

    def _step_factory_and_update(
        self, value: Dataset | Model | int | float | str | None = None
    ) -> Step | StepString | StepNumber | StepDataset:
        # TODO cyclic imports
        from vectice.models.dataset import Dataset
        from vectice.models.model import Model
        from vectice.models.step_dataset import StepDataset
        from vectice.models.step_image import StepImage
        from vectice.models.step_number import StepNumber
        from vectice.models.step_string import StepString

        if isinstance(value, (int, float)):
            self._update_iteration_step(StepType.StepNumber, value)
            return StepNumber(step=self, number=value)

        if (
            isinstance(value, Image)
            or isinstance(value, IOBase)
            or (isinstance(value, str) and _check_image_path(value))
        ):
            step_artifacts, filename = self._create_image_artifact(value)
            self._update_iteration_step(StepType.StepImage, value, step_artifacts)
            _logger.info(f"File {filename!r} linked to Step {self.name!r}.")
            return StepImage(self, value)

        if isinstance(value, str):
            self._update_iteration_step(StepType.StepString, value)
            return StepString(self, string=value)

        if isinstance(value, Model):
            self._client.update_iteration_step_artifact(
                self.id,
                StepType.StepModel,
            )
            self._warn_step_change(value)
            self.model = value
            step = self._refresh_step()
            step._model = value
            return step

        if isinstance(value, Dataset):
            code_version_id = self._get_code_version_id()
            data = self._client.register_dataset_from_source(
                dataset=value,
                project_id=self.project.id,
                phase_id=self.phase.id,
                iteration_id=self.iteration.id,
                code_version_id=code_version_id,
            )
            existing_dataset_logger(data, value.name, _logger)
            artifacts = [
                IterationStepArtifactInput(
                    id=data["datasetVersion"]["id"],
                    type=IterationStepArtifactType.DataSetVersion.name,
                )
            ]
            step_output = self._client.update_iteration_step_artifact(
                self.id,
                StepType.StepDataset,
                None,
                artifacts,
            )
            _logger.info(
                f"Successfully added Dataset(name='{value.name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type=MODELING) to {step_output.name}"
            )
            self.artifacts = [IterationStepArtifact(datasetVersionId=step_output.id, type="DataSetVersion")]
            self._warn_step_change(value)
            return StepDataset(self, dataset_version=step_output.artifacts[0])

        return self

    def _create_image_artifact(self, value: str | IOBase | Image) -> tuple[list[IterationStepArtifactInput], str]:
        image, filename = _get_image_variables(value)
        try:
            attachments_output = self._client.create_phase_attachments(
                [("file", (filename, image))], self.phase.id, self.project.id
            )
            return [
                IterationStepArtifactInput(id=artifact["fileId"], type="EntityFile") for artifact in attachments_output
            ], filename
        except Exception as error:
            raise ValueError("Check the provided image.") from error

    def _keep_artifacts(self, artifacts: list[IterationStepArtifact]) -> list[IterationStepArtifactInput]:
        def _get_artifact_id(artifact: IterationStepArtifact) -> int:
            if artifact.model_version_id:
                return artifact.model_version_id
            if artifact.dataset_version_id:
                return artifact.dataset_version_id
            if artifact.entity_file_id:
                return artifact.entity_file_id
            raise ValueError("No artifact ID.")

        return [
            IterationStepArtifactInput(id=_get_artifact_id(artifact), type=artifact.type.value)
            for artifact in artifacts
        ]

    def _update_iteration_step(
        self, type: StepType, value, step_artifacts: list[IterationStepArtifactInput] | None = None
    ):
        # TODO: cyclic import
        from vectice.models.model import Model

        if type is StepType.StepImage:
            self._client.update_iteration_step_artifact(
                self.id,
                type,
                None,
                artifacts=step_artifacts or [],
            )
            self._warn_step_change(StepType.StepImage)
        elif isinstance(value, (str, int, float)):
            maintain_artifacts = self._keep_artifacts(
                self._client.get_step(self.id, self.phase.id, self.iteration.index).artifacts
            )
            self._client.update_iteration_step_artifact(
                self.id,
                type,
                str(value),
                maintain_artifacts,
            )

            self._warn_step_change(value)
        elif isinstance(value, Model) or type is StepType.StepModel:
            self._client.update_iteration_step_artifact(self.id, StepType.StepModel, artifacts=step_artifacts)
            self._warn_step_change(value)
            self.model = value
        elif type is StepType.StepDataset:
            self._client.update_iteration_step_artifact(self.id, StepType.StepDataset, artifacts=step_artifacts)
            self._warn_step_change(value)

    def _warn_step_change(self, value):
        # TODO: cyclic import
        from vectice.models.dataset import Dataset
        from vectice.models.model import Model

        if self._type is StepType.Step:
            return
        elif self._type is not StepType.StepModel and isinstance(value, Model):
            _logger.info(f"Step type changed from {self._type.name} to StepModel")
        elif self._type is not StepType.StepDataset and isinstance(value, Dataset):
            _logger.info(f"Step type changed from {self._type.name} to StepDataset")
        elif self._type is not StepType.StepImage and StepType.StepImage is value:
            _logger.info(f"Step type changed from {self._type.name} to StepImage")
        elif self._type is not StepType.StepNumber and isinstance(value, (int, float)):
            _logger.info(f"Step type changed from {self._type.name} to StepNumber")
        elif self._type is not StepType.StepString and isinstance(value, str):
            _logger.info(f"Step type changed from {self._type.name} to StepString")

    @property
    def name(self) -> str:
        """The step's name.

        Returns:
            The step's name.
        """
        return self._name

    @property
    def id(self) -> int:
        """The step's id.

        Returns:
            The step's id.
        """
        return self._id

    @id.setter
    def id(self, step_id: int):
        """Set the step's id.

        Parameters:
            step_id: The id to set.
        """
        self._id = step_id

    @property
    def index(self) -> int:
        """The step's index.

        Returns:
            The step's index.
        """
        return self._index

    @property
    def slug(self) -> str:
        """The step's slug.

        Returns:
            The step's slug.
        """
        return self._slug

    @property
    def properties(self) -> dict:
        """The step's name, id, and index.

        Returns:
            A dictionary containing the `name`, `id` and `index` items.
        """
        return {"name": self.name, "id": self.id, "index": self.index}

    @property
    @deprecate(
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'completed' property is deprecated. "
        "Use 'iteration.completed' instead. "
        "Using 'completed' will raise an error in v{fail_at}. "
        "The property will be removed in v{remove_at}.",
    )
    def completed(self) -> bool:
        """Whether this step is completed.

        Warning: Deprecated since 23.1:
            Use [`Iteration.completed`][vectice.models.iteration.Iteration.completed] instead,
            or simply check that a step has a value / is not `None`.

            To support previous Vectice versions (22.4), this property will
            return True if the step was previously marked as complete.
            For new Vectice versions (23.1+), and steps that haven't been marked
            as complete, this property returns whether the iteration is completed.

        Returns:
            Whether this step is completed.
        """
        if self._completed is None:
            return self._iteration.completed
        return self._completed

    @property
    def artifacts(self) -> list[IterationStepArtifact]:
        return self._artifacts

    @artifacts.setter
    def artifacts(self, artifacts: list[IterationStepArtifact]):
        self._artifacts = artifacts

    @property
    def text(self) -> str | None:
        """The step's text.

        A string that is stored in the step.

        Returns:
            The step's text.
        """
        return self._text

    @deprecate(
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'next_step' method is deprecated. "
        "Using 'next_step' will raise an error in v{fail_at}. "
        "The method will be removed in v{remove_at}.",
    )
    def next_step(self, message: str | None = None) -> Step | None:
        """Deprecated. Advance to the next step.

        Close the current step (mark it completed) and return the next
        step to complete if another open step exists. Otherwise return None.

        Note that steps are not currently ordered, and so the concept
        of "next" is rather arbitrary.

        Parameters:
            message: The message to use when closing the current step.

        Returns:
            The next step.
        """
        try:
            self.close(message)
        except VecticeException:
            _logger.warning("The step is closed!")
            return None
        steps_output = self._client.list_steps(self._iteration._phase.id, self._iteration.index)
        open_steps = sorted(
            [
                Step(item.id, self._iteration, item.name, item.index, item.slug, item.description)
                for item in steps_output
                if not item.completed
            ],
            key=lambda x: x.index,
        )
        if not open_steps:
            _logger.warning("There are no active steps.")
            return None
        next_step = open_steps[0]
        _logger.info(f"Next step : {repr(next_step)}")
        return next_step

    @deprecate(
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'close' method is deprecated. "
        "Using 'close' will raise an error in v{fail_at}. "
        "The method will be removed in v{remove_at}.",
    )
    def close(self, message: str | None = None):
        """Deprecated. Close the current step, marking it completed.

        Parameters:
            message: The message to use when closing the step.
        """
        self._client.close_step(self.id, message)
        _logger.info(f"'{self.name}' was successfully closed.")
        self._completed = True

    @property
    def connection(self) -> Connection:
        """The connection to which this step belongs.

        Returns:
            The connection to which this step belongs.
        """
        return self._iteration.connection

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this step belongs.

        Returns:
            The workspace to which this step belongs.
        """
        return self._iteration.workspace

    @property
    def project(self) -> Project:
        """The project to which this step belongs.

        Returns:
            The project to which this step belongs.
        """
        return self._iteration.project

    @property
    def phase(self) -> Phase:
        """The phase to which this step belongs.

        Returns:
            The phase to which this step belongs.
        """
        return self._iteration.phase

    @property
    def iteration(self) -> Iteration:
        """The iteration to which this step belongs.

        Returns:
            The iteration to which this step belongs.
        """
        return self._iteration

    @property
    @deprecate(
        warn_at="23.1",
        fail_at="23.3",
        remove_at="23.4",
        reason="The `origin_dataset` getter is deprecated. "
        "You should assign and retrieve datasets directly to/from steps instead. "
        "This getter will fail at v{fail_at} and be removed in v{remove_at}.",
    )
    def origin_dataset(self) -> Dataset | None:
        """Deprecated. The step's origin dataset.

        WARNING: **Deprecated.**
        Assign and retrieve datasets directly to/from steps instead.

        Returns:
            The origin dataset, or None if there is none.
        """
        return self._origin_dataset

    @origin_dataset.setter
    @deprecate(
        warn_at="23.1",
        fail_at="23.3",
        remove_at="23.4",
        reason="The `origin_dataset` setter is deprecated. "
        "You should assign and retrieve datasets directly to/from steps instead. "
        "This getter will fail at v{fail_at} and be removed in v{remove_at}.",
    )
    def origin_dataset(self, wrapper: DataWrapper) -> None:
        """Deprecated. Set the step's origin dataset    .

        Typical usage example:

        ```python
        my_iteration = my_phase.iteration()
        my_iteration.step_origin.origin_dataset = my_dataset
        ```

        Parameters:
            dataset: The origin dataset.
        """
        dataset = wrapper_to_dataset(wrapper)
        self._origin_dataset = dataset
        _check_read_only(self.iteration)
        dataset_artifact, data = self._register_dataset(dataset)
        dataset_artifact_input = IterationStepArtifactInput(
            id=dataset_artifact.dataset_version_id, type=dataset_artifact.type.value
        )
        self._manage_dataset_artifact_update(dataset_artifact)
        link_dataset_to_step(dataset_artifact_input, dataset, data, _logger, self)

    @property
    @deprecate(
        warn_at="23.1",
        fail_at="23.3",
        remove_at="23.4",
        reason="The `clean_dataset` getter is deprecated. "
        "You should assign and retrieve datasets directly to/from steps instead. "
        "This getter will fail at v{fail_at} and be removed in v{remove_at}.",
    )
    def clean_dataset(self) -> Dataset | None:
        """Deprecated. The step's cleaned dataset.

        WARNING: **Deprecated.**
        Assign and retrieve datasets directly to/from steps instead.

        Returns:
            The step's cleaned dataset, or None.
        """
        return self._clean_dataset

    @clean_dataset.setter
    @deprecate(
        warn_at="23.1",
        fail_at="23.3",
        remove_at="23.4",
        reason="The `clean_dataset` setter is deprecated. "
        "You should assign and retrieve datasets directly to/from steps instead. "
        "This getter will fail at v{fail_at} and be removed in v{remove_at}.",
    )
    def clean_dataset(self, wrapper: DataWrapper) -> None:
        """Deprecated. Set the step's cleaned dataset.

        Typical usage example:

        ```python
        my_iteration = my_phase.iteration()
        my_iteration.step_cleaning.clean_dataset = my_dataset
        ```

        Parameters:
            dataset: The cleaned dataset.
        """
        dataset = wrapper_to_dataset(wrapper)
        self._clean_dataset = dataset
        _check_read_only(self.iteration)
        dataset_artifact, data = self._register_dataset(dataset)
        dataset_artifact_input = IterationStepArtifactInput(
            id=dataset_artifact.dataset_version_id, type=dataset_artifact.type.value
        )
        self._manage_dataset_artifact_update(dataset_artifact)
        link_dataset_to_step(dataset_artifact_input, dataset, data, _logger, self)

    @property
    @deprecate(
        warn_at="23.1",
        fail_at="23.3",
        remove_at="23.4",
        reason="The `modeling_dataset` getter is deprecated. "
        "You should assign and retrieve datasets directly to/from steps instead. "
        "This getter will fail at v{fail_at} and be removed in v{remove_at}.",
    )
    def modeling_dataset(self) -> Dataset | None:
        """Deprecated. The step's modeling dataset.

        WARNING: **Deprecated.**
        Assign and retrieve datasets directly to/from steps instead.

        Returns:
            The training set, the test set and the validation set if it exists.
        """
        return self._modeling_dataset

    @modeling_dataset.setter
    @deprecate(
        warn_at="23.1",
        fail_at="23.3",
        remove_at="23.4",
        reason="The `modeling_dataset` setter is deprecated. "
        "You should assign and retrieve datasets directly to/from steps instead. "
        "This getter will fail at v{fail_at} and be removed in v{remove_at}.",
    )
    def modeling_dataset(self, wrapper: tuple[DataWrapper, ...]) -> None:
        """Deprecated. Set the step's modeling dataset.

        Provides training, testing and optional validation datasources, the
        order of which does not matter (despite it being a tuple) and
        the combination of the data sources does not either. Thus, you
        could use whatever combination suites your needs.

        The resource can be accessed via `vectice.FileResource`,
        `vectice.GCSResource` and `vectice.S3Resource`.

        Or for example `from vectice import FileResource`.

        Typical usage example:

        ```python
        my_iteration = my_phase.iteration()
        my_iteration.step_modeling.modeling_dataset = my_dataset
        ```

        Parameters:
            dataset: A modeling dataset.
        """
        dataset = wrapper_to_dataset(wrapper)
        self._modeling_dataset = dataset
        _check_read_only(self.iteration)
        logging.getLogger("vectice.models.iteration").propagate = True

        dataset_artifact, data = self._register_dataset(dataset)
        dataset_artifact_input = IterationStepArtifactInput(
            id=dataset_artifact.dataset_version_id, type=dataset_artifact.type.value
        )
        self._manage_dataset_artifact_update(dataset_artifact)
        link_assets_to_step(self, dataset_artifact_input, dataset.name, data, _logger)

    @staticmethod
    def _get_datasources_in_order(data_sources: tuple[Resource, ...]) -> tuple[Resource, Resource, Resource | None]:
        from vectice import DatasetSourceUsage

        if len(data_sources) != 3 and len(data_sources) != 2:
            raise ValueError("Exactly two or three datasources are needed to create a modeling dataset.")

        train_datasource, test_datasource, validation_datasource = None, None, None
        for data_source in data_sources:
            if data_source:
                if data_source.metadata.usage == DatasetSourceUsage.TRAINING:
                    train_datasource = data_source
                elif data_source.metadata.usage == DatasetSourceUsage.TESTING:
                    test_datasource = data_source
                elif data_source.metadata.usage == DatasetSourceUsage.VALIDATION:
                    validation_datasource = data_source
        if not train_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "training")
        if not test_datasource:
            raise ValueError(MISSING_DATASOURCE_ERROR_MESSAGE % "testing")
        return train_datasource, test_datasource, validation_datasource

    def _get_code_version_id(self):
        # TODO: cyclic imports
        from vectice.models.git_version import _check_code_source, _inform_if_git_repo

        if vectice.code_capture:
            return _check_code_source(self._client, self.project.id, _logger)
        else:
            _inform_if_git_repo()
            return None

    @property
    def model(self) -> Model | None:
        """The step's model.

        Returns:
            The step's model.
        """
        return self._model

    @model.setter
    def model(self, model: Model):
        """Set the model for the step.

        The model can be created using the Model Wrapper, accessed via
        vectice.Model or `from vectice import Model`.

        Parameters:
            model: The model.
        """
        model_artifact = self._register_model(model)
        self._model = model
        self.artifacts = [model_artifact]

    def _set_model_attachments(self, model: Model, model_version: ModelVersionOutput):
        logging.getLogger("vectice.models.attachment_container").propagate = True
        attachments = None
        if model.attachments:
            container = AttachmentContainer(model_version, self._client)
            attachments = container.add_attachments(model.attachments)
        if model.predictor:
            model_content = self._serialize_model(model.predictor)
            model_type_name = type(model.predictor).__name__
            container = AttachmentContainer(model_version, self._client)
            container.add_serialized_model(model_type_name, model_content)
        return attachments

    @staticmethod
    def _serialize_model(model: Any) -> bytes:
        return pickle.dumps(model)

    def _register_model(self, model: Model) -> IterationStepArtifact:
        from vectice.models.git_version import _check_code_source, _inform_if_git_repo

        _check_read_only(self._iteration)
        if vectice.code_capture:
            code_version_id = _check_code_source(self._client, self._iteration._phase._project._id, _logger)
        else:
            _inform_if_git_repo()
            code_version_id = None
        model_output = self._client.register_model(
            model, self.iteration.project.id, self.phase.id, self.iteration.id, code_version_id, model.derived_from
        )
        model_version = model_output.model_version
        attachments = self._set_model_attachments(model, model_version)
        _logger.info(
            f"Successfully registered Model(name='{model.name}', library='{model.library}', "
            f"technique='{model.technique}', version='{model_version.name}')."
        )
        existing_model_logger(model_output, model.name, _logger)
        step_artifact = IterationStepArtifactInput(id=model_output["modelVersion"]["id"], type="ModelVersion")
        attachments = (
            [
                IterationStepArtifactInput(id=attach["fileId"], entityFileId=attach["entityId"], type="EntityFile")
                for attach in attachments
            ]
            if attachments
            else None
        )
        logging.getLogger("vectice.models.project").propagate = False
        link_assets_to_step(self, step_artifact, model.name, model_output, _logger, attachments)
        model_artifact = IterationStepArtifact(modelVersionId=step_artifact.id, type=step_artifact.type)
        return model_artifact

    def _register_dataset(self, dataset: Dataset) -> tuple[IterationStepArtifact, dict]:
        _check_read_only(self.iteration)
        code_version_id = self._get_code_version_id()

        data = self._client.register_dataset_from_source(
            dataset=dataset,
            project_id=self.project.id,
            phase_id=self.phase.id,
            iteration_id=self.iteration.id,
            code_version_id=code_version_id,
        )
        existing_dataset_logger(data, dataset.name, _logger)
        step_artifact = IterationStepArtifactInput(id=data["datasetVersion"]["id"], type="DataSetVersion")
        logging.getLogger("vectice.models.iteration").propagate = False
        logging.getLogger("vectice.models.project").propagate = False

        if dataset.type is DatasetType.MODELING:
            link_assets_to_step(self, step_artifact, dataset.name, data, _logger)
        else:
            link_dataset_to_step(step_artifact, dataset, data, _logger, self)
        dataset_artifact = IterationStepArtifact(datasetVersionId=step_artifact.id, type=step_artifact.type)
        return dataset_artifact, data

    def _manage_dataset_artifact_update(self, step_artifact: IterationStepArtifact):
        self.artifacts.append(step_artifact)
        refreshed_step = self._refresh_step()
        if refreshed_step._type is not StepType.StepDataset:
            _logger.warning(f"Step: {self.name!r} type changed from {self._type.name} to StepDataset")
