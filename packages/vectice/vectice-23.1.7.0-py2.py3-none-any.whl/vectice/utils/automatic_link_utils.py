from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.api.json.iteration import IterationStepArtifact, IterationStepArtifactInput, IterationStepArtifactType
from vectice.models.dataset import Dataset
from vectice.models.datasource.datawrapper import FileDataWrapper, GcsDataWrapper, S3DataWrapper
from vectice.models.datasource.datawrapper.data_wrapper import DataWrapper
from vectice.models.resource import FileResource, GCSResource, S3Resource
from vectice.models.resource.metadata import DatasetSourceUsage, DatasetType
from vectice.utils.deprecation import ignore_deprecation_warnings

if TYPE_CHECKING:
    from logging import Logger

    from vectice.models import Step
    from vectice.models.resource.base import Resource


def existing_dataset_logger(data: dict, dataset_name: str, _logger: Logger):
    if data["useExistingDataset"]:
        existing_dataset_version = f"Dataset: {dataset_name}"
        if data["useExistingVersion"]:
            existing_dataset_version += f" with Version: {data['datasetVersion']['name']}"
        _logger.debug(f"{existing_dataset_version} already exists.")


def existing_model_logger(data: dict, model_name: str, _logger: Logger):
    if data["useExistingModel"]:
        _logger.info(f"Model: {model_name} already exists.")


def link_dataset_to_step(
    step_artifact: IterationStepArtifactInput,
    dataset: Dataset,
    data: dict,
    _logger: Logger,
    step: Step,
):
    """Link a dataset to a step.

    1. We get the current phase if it exists
        - No phase results in a warning / failure (we can't assume phases are ordinal so this fails/exits)
        - We need a phase to be called at some point at the very least
    2. We get the current iteration if it exists (e.g. a user did `phase.iteration()`)
        - No iteration results in us getting one/creating one.
    3. We get the current step if it exists (e.g. a user did `iteration.step()`)
    3. If there is no current step
        - We check if the iteration has any steps that are not completed

    Parameters:
        step_artifact: The artifact to link.
        dataset: The dataset.
        data: The artifact metadata.
        step: The step to link to.
    """
    client = step._client
    step_artifacts = get_updated_step_artifacts(step, _logger)
    dataset_type_name = dataset.type.name
    matching_datasets = [
        artifact
        for artifact in step_artifacts
        if artifact.type == IterationStepArtifactType.DataSetVersion and artifact.dataset_version_id == step_artifact.id
    ]
    if datasets_are_new_in_step(step_artifacts, matching_datasets):
        step_output = client.add_iteration_step_artifact(step.id, step_artifact)
        _logger.info(
            f"Successfully added Dataset(name='{dataset.name}', id={data['datasetVersion']['id']}, "
            f"version='{data['datasetVersion']['name']}', type={dataset_type_name}) to {step_output.name}"
        )
    elif datasets_already_exist_in_step(step_artifacts, matching_datasets):
        _logger.info(
            f"The step {step.name} already has Dataset(name='{dataset.name}', id={data['datasetVersion']['id']}, "
            f"version='{data['datasetVersion']['name']}', type={dataset_type_name}) linked."
        )
    else:
        _logger.warning(
            f"There are no active steps to attach the registered Dataset(name='{dataset.name}', id={data['datasetVersion']['id']}, "
            f"version='{data['datasetVersion']['name']}', type={dataset_type_name}) to."
        )


def get_updated_step_artifacts(step: Step, _logger: Logger):
    iteration = step.iteration
    refresh_step = iteration.step(step.name)
    with ignore_deprecation_warnings():
        if not refresh_step.completed:
            return refresh_step.artifacts
    return []


def datasets_are_new_in_step(
    step_artifacts: list[IterationStepArtifact], matching_datasets: list[IterationStepArtifact]
):
    return len(step_artifacts) == 0 or (len(step_artifacts) >= 1 and not any(matching_datasets))


def datasets_already_exist_in_step(
    step_artifacts: list[IterationStepArtifact], matching_datasets: list[IterationStepArtifact]
):
    return len(step_artifacts) >= 1 and any(matching_datasets)


def link_assets_to_step(
    step: Step,
    step_artifact: IterationStepArtifactInput,
    name: str,
    data: dict,
    _logger: Logger,
    attachments: list[IterationStepArtifactInput] | None = None,
):
    """Link assets to a step.

    The step is refreshed, the step status is checked and the link and logger is used for the relevant artifact.

    Parameters:
        step: The current step.
        step_artifact: A step artifact to link.
        name: The resulting dataset name.
        data: The dataset metadata dictionary.
        attachments: Additional artifact to link.

    Raises:
        RuntimeError: When the step artifact type is neither `DataSetVersion` or `ModelVersion`.
    """
    client = step._client
    refresh_step = step._iteration.step(step.name)
    with ignore_deprecation_warnings():
        refresh_step_completed = refresh_step and refresh_step.completed
    if refresh_step and not refresh_step_completed:
        step_id, step_name = refresh_step.id, refresh_step.name
        step_artifacts = refresh_step.artifacts
    else:
        raise RuntimeError(f"The step: {step.name} is not active!")
    if step_artifact.type == IterationStepArtifactType.DataSetVersion.value:
        _dataset_link_and_logger(client, step_artifact, step_artifacts, name, data, step_name, step_id, _logger)
    elif step_artifact.type == IterationStepArtifactType.ModelVersion.value:
        _model_link_and_logger(client, step_artifact, step_artifacts, name, data, step_name, step_id, _logger)
    else:
        raise RuntimeError("Vectice Error: The step artifact type was not set.")
    if attachments:
        _attachment_link_and_logger(client, attachments, step_artifacts, name, data, step_name, step_id, _logger)


def _dataset_link_and_logger(
    client,
    step_artifact: IterationStepArtifactInput,
    step_artifacts: list[IterationStepArtifact],
    name: str,
    data: dict,
    step_name: str,
    step_id: int,
    _logger: Logger,
):
    check_assets = [artifact for artifact in step_artifacts if artifact.type == IterationStepArtifactType.ModelVersion]
    match_dataset_assets = [
        artifact
        for artifact in step_artifacts
        if artifact.type == IterationStepArtifactType.DataSetVersion and artifact.dataset_version_id == step_artifact.id
    ]
    if (len(step_artifacts) == 0 or len(step_artifacts) == len(check_assets)) or (
        len(step_artifacts) >= 1 and not any(match_dataset_assets)
    ):
        step_output = client.add_iteration_step_artifact(step_id, step_artifact)
        _logger.info(
            f"Successfully added Dataset(name='{name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type=MODELING) to {step_output.name}"
        )
    elif len(step_artifacts) >= 1 and any(match_dataset_assets):
        _logger.info(
            f"The step {step_name} already has Dataset(name='{name}', id={data['datasetVersion']['id']}, version='{data['datasetVersion']['name']}', type=MODELING) linked."
        )
    else:
        raise RuntimeError("Vectice Error: The dataset link failed")


def _model_link_and_logger(
    client,
    step_artifact: IterationStepArtifactInput,
    step_artifacts: list[IterationStepArtifact],
    name: str,
    data: dict,
    step_name: str,
    step_id: int,
    _logger: Logger,
):
    check_assets = [
        artifact for artifact in step_artifacts if artifact.type == IterationStepArtifactType.DataSetVersion
    ]
    match_model_assets = [
        artifact
        for artifact in step_artifacts
        if artifact.type == IterationStepArtifactType.ModelVersion and artifact.model_version_id == step_artifact.id
    ]
    if (len(step_artifacts) == 0 or len(step_artifacts) == len(check_assets)) or (
        len(step_artifacts) >= 1 and not any(match_model_assets)
    ):
        step_output = client.add_iteration_step_artifact(step_id, step_artifact)
        _logger.info(
            f"Successfully added Model(name='{name}', version='{data['modelVersion']['name']}') to {step_output.name}"
        )
    elif len(step_artifacts) >= 1 and any(match_model_assets):
        _logger.info(
            f"The step {step_name} already has Model(name='{name}', version='{data['modelVersion']['name']}') linked."
        )
    else:
        raise RuntimeError("Vectice Error: The model link failed")


def _attachment_link_and_logger(
    client,
    attachments: list[IterationStepArtifactInput],
    step_artifacts: list[IterationStepArtifact],
    name: str,
    data: dict,
    step_name: str,
    step_id: int,
    _logger: Logger,
):
    check_assets = [artifact for artifact in step_artifacts if artifact.type == IterationStepArtifactType.EntityFile]
    for attachment in attachments:
        match_attachment_assets = [
            artifact
            for artifact in step_artifacts
            if artifact.type == IterationStepArtifactType.EntityFile
            and artifact.entity_file_id == attachment.entity_file_id
        ]
        if (len(step_artifacts) == 0 or len(step_artifacts) == len(check_assets)) or (
            len(step_artifacts) >= 1 and not any(match_attachment_assets)
        ):
            attachment.pop("entityFileId")
            step_output = client.add_iteration_step_artifact(step_id, attachment)
            _logger.info(
                f"Successfully added Attachment: {attachment.id} from Model(name='{name}', version='{data['modelVersion']['name']}') to {step_output.name}"
            )
        elif len(step_artifacts) >= 1 and any(match_attachment_assets):
            _logger.info(
                f"The step {step_name} already has Attachment: {attachment.id} from Model(name='{name}', version='{data['modelVersion']['name']}') linked."
            )
        else:
            raise RuntimeError("Vectice Error: The attachment link failed")


def wrapper_to_resource(wrapper: DataWrapper) -> Resource:
    if isinstance(wrapper, FileDataWrapper):
        return FileResource(path=wrapper.path)
    elif isinstance(wrapper, GcsDataWrapper):
        return GCSResource(
            gcs_client=wrapper.gcs_client,
            bucket_name=wrapper.bucket_name,
            resource_paths=wrapper.resource_paths,
        )
    elif isinstance(wrapper, S3DataWrapper):
        return S3Resource(
            s3_client=wrapper.s3_client,
            bucket_name=wrapper.bucket_name,
            resource_path=wrapper.resource_path,
        )
    raise ValueError(f"Unhandled wrapper type: {wrapper.__class__}")


def wrapper_to_dataset(wrapper: DataWrapper | tuple[DataWrapper, ...]) -> Dataset:
    if isinstance(wrapper, DataWrapper):
        return Dataset(
            type=wrapper.type,
            name=wrapper.name,
            resource=wrapper_to_resource(wrapper),
            derived_from=wrapper.derived_from,  # type: ignore[arg-type]
        )

    derived_from = []
    training_resource = testing_resource = validation_resource = None
    for wrap in wrapper:
        if wrap.usage is DatasetSourceUsage.TRAINING:
            training_resource = wrapper_to_resource(wrap)
        elif wrap.usage is DatasetSourceUsage.TESTING:
            testing_resource = wrapper_to_resource(wrap)
        elif wrap.usage is DatasetSourceUsage.VALIDATION:
            validation_resource = wrapper_to_resource(wrap)
        if wrap.derived_from:
            derived_from.extend(wrap.derived_from)
    return Dataset(
        type=DatasetType.MODELING,
        name=wrapper[0].name,
        training_resource=training_resource,
        testing_resource=testing_resource,
        validation_resource=validation_resource,
        derived_from=derived_from,  # type: ignore[arg-type]
    )
