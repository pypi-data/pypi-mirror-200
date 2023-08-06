from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, BinaryIO

from gql import Client as GQLClient
from gql.transport.requests import RequestsHTTPTransport

from vectice.__version__ import __version__
from vectice.api._auth import Auth
from vectice.api.attachment import AttachmentApi
from vectice.api.compatibility import CompatibilityApi
from vectice.api.gql_code import GqlCodeApi
from vectice.api.gql_code_version import GqlCodeVersionApi
from vectice.api.gql_dataset import GqlDatasetApi
from vectice.api.gql_model import GqlModelApi
from vectice.api.gql_user_workspace_api import UserAndDefaultWorkspaceApi
from vectice.api.http_error_handlers import MissingReferenceError, StepIdError, StepNameError
from vectice.api.iteration import IterationApi
from vectice.api.json import (
    ArtifactName,
    CodeInput,
    CodeVersionCreateBody,
    ModelRegisterInput,
    ModelRegisterOutput,
    ModelType,
    ModelVersionOutput,
    ModelVersionStatus,
    Page,
    PagedResponse,
    ProjectInput,
    PropertyInput,
    StepOutput,
)
from vectice.api.json.dataset_register import DatasetRegisterInput, DatasetRegisterOutput
from vectice.api.json.metric import MetricInput
from vectice.api.json.step import StepUpdateInput
from vectice.api.last_assets import LastAssetApi
from vectice.api.phase import PhaseApi
from vectice.api.project import ProjectApi
from vectice.api.step import StepApi
from vectice.api.version import VersionApi
from vectice.api.workspace import WorkspaceApi
from vectice.models.dataset import Dataset
from vectice.utils.deprecation import deprecate

if TYPE_CHECKING:
    from io import BytesIO, IOBase

    from requests import Response

    from vectice.api.json import AttachmentOutput, ProjectOutput, WorkspaceOutput
    from vectice.api.json.compatibility import CompatibilityOutput
    from vectice.api.json.iteration import IterationInput, IterationOutput, IterationStepArtifactInput
    from vectice.api.json.phase import PhaseOutput
    from vectice.api.json.step import StepType
    from vectice.api.json.workspace import WorkspaceInput
    from vectice.models.model import Model


_logger = logging.getLogger(__name__)


def _auth_success_message(workspace: WorkspaceOutput, project: ProjectOutput | None) -> str:
    if workspace and project:
        return f"Successfully authenticated. You'll be working on Project: '{project.name}', part of Workspace: '{workspace.name}'"
    return f"Successfully authenticated. Your current Workspace: '{workspace.name}'"


class Client:
    """Low level Vectice API client."""

    def __init__(
        self,
        workspace: str | int | None = None,
        project: str | int | None = None,
        token: str | None = None,
        api_endpoint: str | None = None,
        auto_connect=True,
        allow_self_certificate=True,
    ):
        self.auth = Auth(
            api_endpoint=api_endpoint,
            api_token=token,
            auto_connect=auto_connect,
            allow_self_certificate=allow_self_certificate,
        )
        transport = RequestsHTTPTransport(url=self.auth.api_base_url + "/graphql", verify=self.auth.verify_certificate)
        logging.getLogger("gql.transport.requests").setLevel("WARNING")
        self._gql_client = GQLClient(transport=transport)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._workspace = None
        self._project = None

        if auto_connect:
            if workspace and project:
                self._project = self.get_project(project, workspace)
                self._workspace = self._project.workspace
                if (
                    isinstance(workspace, str)
                    and workspace != self._workspace.name
                    or isinstance(workspace, int)
                    and workspace != self._workspace.id
                ):
                    raise ValueError(
                        f"Inconsistency in configuration: Project {project} does not belong to Workspace {workspace}"
                    )
            elif workspace:
                self._workspace = self.get_workspace(workspace)
            elif project:
                self._project = self.get_project(project)
                self._workspace = self._project.workspace

            if self._workspace:
                _logger.debug(_auth_success_message(workspace=self._workspace, project=self._project))

    @property
    def workspace(self) -> WorkspaceOutput | None:
        """The workspace object.

        Returns:
            The workspace object.
        """
        return self._workspace

    @property
    def project(self) -> ProjectOutput | None:
        """The project object.

        Returns:
            The project object.
        """
        return self._project

    @property
    def version_api(self) -> str:
        return __version__

    @property
    def version_backend(self) -> str:
        versions = VersionApi(self._gql_client, self.auth).get_public_config().versions
        for version in versions:
            if version.artifact_name == ArtifactName.BACKEND:
                return version.version
        raise ValueError("No version found for backend.")

    def check_compatibility(self) -> CompatibilityOutput:
        return CompatibilityApi(self.auth).check_version()

    def create_project(self, data: ProjectInput, workspace: str | int) -> ProjectOutput:
        """Create a project.

        Parameters:
            data: The ProjectInput JSON structure.
            workspace: The workspace name or id.

        Returns:
            The project JSON structure.
        """
        result = ProjectApi(self.auth).create_project(data, workspace)
        _logger.info(f"Project with id: {result.id} successfully created.")
        return result

    def delete_project(self, project: str | int, workspace: str | int | None = None):
        """Delete a project.

        Parameters:
            project: The project name or id.
            workspace: The workspace name or id.
        """
        ProjectApi(self.auth).delete_project(project, workspace)

    def update_project(self, data: ProjectInput, project: str | int, workspace: str | int) -> ProjectOutput:
        """Update a project.

        Parameters:
            data: The ProjectInput JSON structure.
            project: The project name or id.
            workspace: The workspace name or id.

        Returns:
            The project JSON structure.
        """
        return ProjectApi(self.auth).update_project(data, project, workspace)

    def list_projects(
        self,
        workspace: str | int,
        search: str | None = None,
        page_index: int | None = Page.index,
        page_size: int | None = Page.size,
    ) -> PagedResponse[ProjectOutput]:
        """List the projects in a workspace.

        Parameters:
            workspace: The workspace name or id.
            search: A text to search for.
            page_index: The index of the page.
            page_size: The size of the page.

        Returns:
            The workspace's projects.
        """
        return ProjectApi(self.auth).list_projects(workspace, search, page_index, page_size)

    def get_project(self, project: str | int, workspace: str | int | None = None) -> ProjectOutput:
        """Get a project.

        Parameters:
            project: The project name or id.
            workspace: The workspace name or id.

        Returns:
            The project JSON structure.
        """
        return ProjectApi(self.auth).get_project(project, workspace)

    def get_workspace(self, workspace: str | int) -> WorkspaceOutput:
        """Get a workspace.

        Parameters:
            workspace: The workspace name or id.

        Returns:
            The workspace JSON structure.
        """
        return WorkspaceApi(self.auth).get_workspace(workspace)

    def create_workspace(self, data: WorkspaceInput) -> WorkspaceOutput:
        """Create a workspace.

        Parameters:
            data: The WorkspaceInput JSON structure.

        Returns:
            The workspace JSON structure.
        """
        result = WorkspaceApi(self.auth).create_workspace(data)
        return result

    def update_workspace(self, data: WorkspaceInput, workspace: str | int) -> WorkspaceOutput:
        """Update a workspace.

        Parameters:
            data: The WorkspaceInput JSON structure.
            workspace: The workspace name or id.

        Returns:
            The workspace JSON structure.
        """
        return WorkspaceApi(self.auth).update_workspace(data, workspace)

    def list_workspaces(
        self, search: str | None = None, page_index: int = 1, page_size: int = 20
    ) -> PagedResponse[WorkspaceOutput]:
        """List the workspaces.

        Parameters:
            search: A text to search for.
            page_index: The index of the page.
            page_size: The size of the page.

        Returns:
            The workspaces.
        """
        return WorkspaceApi(self.auth).list_workspaces(search, page_index, page_size)

    def create_code_attachments(self, files: list[tuple[str, tuple[str, str]]], code_version_id: int, project_id: int):
        """Create an attachment.

        Parameters:
            files: The paths to the files to attach.
            code_version_id: The code version id to attach files to.
            project_id: The project id associated to the code version id.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).create_attachments(files, project_id, code_version_id=code_version_id)

    def create_model_attachments(
        self, files: list[tuple[str, tuple[str, BinaryIO]]], model_version: ModelVersionOutput
    ):
        """Create an attachment.

        Parameters:
            files: The paths to the files to attach.
            model_version: The model version to attach files to.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).post_attachment(files, model_version)

    def create_phase_attachments(
        self, files: list[tuple[str, tuple[str, BytesIO | IOBase]]], phase_id: int, project_id: int
    ) -> list[dict]:
        """Create an attachment.

        Parameters:
            files: The paths to the files to attach.
            phase_id: The phase id to attach files to.
            project_id: The project id to attach files to.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).create_attachments(files, project_id, phase_id=phase_id)

    def create_model_predictor(self, model_type: str, model_content: BytesIO, model_version: ModelVersionOutput):
        """Create a predictor.

        Parameters:
            model_type: The type of model to attach.
            model_content: The binary content of the model.
            model_version: The model version to attach files to.

        Returns:
            The JSON structure.
        """
        return AttachmentApi(self.auth).post_model_predictor(model_type, model_content, model_version)

    def list_attachments(self, model_version: ModelVersionOutput) -> PagedResponse[AttachmentOutput]:
        """List the attachments of an artifact.

        Parameters:
            model_version: The model version to list attachments from.

        Returns:
            The attachments of an artifact.
        """
        return AttachmentApi(self.auth).list_attachments(model_version)

    def list_code_attachments(self, code_version_id: int, project_id: int) -> PagedResponse[AttachmentOutput]:
        """List the attachments of a code version.

        Parameters:
            code_version_id: The id of the code version to list attachments from.
            project_id: The id of the project the code version belongs to.

        Returns:
            A list of attachments that belong to the code version.
        """
        return AttachmentApi(self.auth).list_object_attachments(project_id, code_version_id=code_version_id)

    def list_phase_attachments(self, phase_id: int, project_id: int) -> PagedResponse[AttachmentOutput]:
        """List the attachments of a phase.

        Parameters:
            phase_id: The id of the phase the attachments belongs to.
            project_id: The id of the project the attachments belongs to.

        Returns:
            An attachment.
        """
        return AttachmentApi(self.auth).list_object_attachments(project_id, phase_id=phase_id)

    def get_code_version_attachment(self, code_version_id: int, project_id: int, file_id: int) -> Response:
        """Get the attachment of a code version.

        Parameters:
            code_version_id: The code version id to list attachments from.
            project_id: The project id the code version belongs to.
            file_id: The file id attached to the code version.

        Returns:
            The file attached to the code version.
        """
        return AttachmentApi(self.auth).get_code_version_attachment(code_version_id, project_id, file_id)

    def list_phases(
        self,
        search: str | None = None,
        project: str | int | None = None,
        workspace: str | int | None = None,
    ) -> list[PhaseOutput]:
        project, workspace = self.get_project_and_workspace_references_or_raise_error(project, workspace)
        project_object = self.get_project(project, workspace)
        return PhaseApi(self._gql_client, self.auth).list_phases(project_object.id, search)

    def get_phase(self, phase: str | int, project_id: int | None = None) -> PhaseOutput:
        if project_id is None:
            raise MissingReferenceError("project")
        return PhaseApi(self._gql_client, self.auth).get_phase(phase, project_id)

    def get_step(self, step_reference: str | int, phase_id: int, iteration_id: int) -> StepOutput:
        if phase_id is None:
            raise MissingReferenceError("iteration")
        steps = self.list_steps(phase_id, iteration_id)
        if isinstance(step_reference, int):
            for step in steps:
                if step.id == step_reference:
                    return step
            raise StepIdError(step_reference)
        elif isinstance(step_reference, str):
            for step in steps:
                if step.name == step_reference:
                    return step
            raise StepNameError(step_reference)
        raise ValueError(f"No such step reference '{step_reference}' exists in the phase '{phase_id}'")

    def get_step_by_name(self, step_reference: str, iteration_id: int) -> StepOutput:
        return StepApi(self._gql_client, self.auth).get_step(step_reference, iteration_id)

    def list_steps(
        self,
        phase_id: int,
        iteration_index: int | None = None,
        phase_name: str | None = None,
    ) -> list[StepOutput]:
        if iteration_index:
            return StepApi(self._gql_client, self.auth).list_steps_for_iteration(phase_id, iteration_index, phase_name)
        return StepApi(self._gql_client, self.auth).list_steps(phase_id, phase_name)

    def close_step(self, step_id: int, message: str | None = None) -> StepOutput:
        step_update = StepUpdateInput(text=message)
        return StepApi(self._gql_client, self.auth).close_step(step_id, step_update)

    def add_iteration_step_artifact(self, step_id: int, step_artifacts: IterationStepArtifactInput) -> StepOutput:
        return StepApi(self._gql_client, self.auth).add_iteration_step_artifact(step_artifacts, step_id)

    def update_iteration_step_artifact(
        self,
        step_id: int,
        step_type: StepType,
        text: str | None = None,
        artifacts: list[IterationStepArtifactInput] | None = None,
    ) -> StepOutput:
        return StepApi(self._gql_client, self.auth).update_iteration_step_artifact(step_id, step_type, text, artifacts)

    def list_iterations(self, phase: int) -> list[IterationOutput]:
        return IterationApi(self._gql_client, self.auth).list_iterations(phase)

    def list_step_definitions(self, phase: int) -> list[StepOutput]:
        return PhaseApi(self._gql_client, self.auth).list_step_definitions(phase)

    def get_iteration(self, iteration_id: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_iteration(iteration_id)

    def get_iteration_by_index(self, phase_id: int, index: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_iteration_by_index(phase_id, index)

    def get_iteration_last_assets(self, iteration_id: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).get_iteration_last_assets(iteration_id)

    def create_iteration(self, phase_id: int) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).create_iteration(phase_id)

    def update_iteration(self, iteration_id: int, iteration: IterationInput) -> IterationOutput:
        return IterationApi(self._gql_client, self.auth).update_iteration(iteration, iteration_id)

    def delete_iteration(self, iteration_id: int) -> None:
        IterationApi(self._gql_client, self.auth).delete_iteration(iteration_id)

    def register_dataset_from_source(
        self,
        dataset: Dataset,
        project_id: int | None = None,
        phase_id: int | None = None,
        iteration_id: int | None = None,
        code_version_id: int | None = None,
    ) -> DatasetRegisterOutput:
        name = self.get_dataset_name(dataset)
        derived_from = self.get_dataset_derived_from(dataset)
        if isinstance(dataset.resource, tuple):
            # modeling dataset
            metadata_asdict = [data_source.metadata.asdict() for data_source in dataset.resource if data_source]
        else:
            metadata_asdict = [dataset.resource.metadata.asdict()]

        dataset_register_input = DatasetRegisterInput(
            name=name,
            type=dataset.type.value,
            datasetSources=metadata_asdict,
            inputs=derived_from,
            codeVersionId=code_version_id,
        )
        dataset_register_output = self.register_dataset(dataset_register_input, project_id, phase_id, iteration_id)
        dataset.latest_version_id = dataset_register_output["datasetVersion"]["id"]
        return dataset_register_output

    @staticmethod
    def get_dataset_name(dataset: Dataset) -> str:
        return f"dataset {datetime.time}" if dataset.name is None else dataset.name

    @staticmethod
    @deprecate(
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'get_dataset_inputs' method is renamed 'get_dataset_derived_from'. "
        "Using 'get_dataset_inputs' will raise an error in v{fail_at}. "
        "The method will be removed in v{remove_at}.",
    )
    def get_dataset_inputs(dataset: Dataset) -> list[int]:
        return Client.get_dataset_derived_from(dataset)

    @staticmethod
    def get_dataset_derived_from(dataset: Dataset) -> list[int]:
        return [] if dataset.derived_from is None else dataset.derived_from

    def register_dataset(
        self,
        dataset_register_input: DatasetRegisterInput,
        project_id: int | None = None,
        phase_id: int | None = None,
        iteration_id: int | None = None,
    ) -> DatasetRegisterOutput:
        try:
            data: DatasetRegisterOutput = GqlDatasetApi(self._gql_client, self.auth).register_dataset(
                dataset_register_input, project_id, phase_id, iteration_id
            )
            _logger.info(
                f"Successfully registered Dataset("
                f"name='{dataset_register_input.name}', "
                f"id={data['datasetVersion']['id']}, "
                f"version='{data['datasetVersion']['name']}', "
                f"type={dataset_register_input.type})."
            )
            return data
        except Exception as e:
            raise ValueError(f"The dataset register failed due to {e}") from e

    def get_project_and_workspace_references(
        self, project: str | int | None = None, workspace: str | int | None = None
    ):
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return project, workspace

    def get_project_and_workspace_refs_if_project_ref_is_str(
        self, project: str | int | None = None, workspace: str | int | None = None
    ):
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return project, workspace

    def get_project_and_workspace_refs_if_project_ref_is_str_or_raise_error(
        self, project: str | int | None = None, workspace: str | int | None = None
    ) -> tuple[str | int, str | int | None]:
        project, workspace = self.get_project_and_workspace_refs_if_project_ref_is_str(project, workspace)
        if project is None:
            raise MissingReferenceError("project")
        return project, workspace

    def get_project_and_workspace_references_or_raise_error(
        self, project: str | int | None = None, workspace: str | int | None = None
    ) -> tuple[str | int, str | int | None]:
        project, workspace = self.get_project_and_workspace_references(project, workspace)
        if project is None:
            raise MissingReferenceError("project")
        return project, workspace

    @staticmethod
    def _get_model_name(library: str, technique: str, name: str | None = None) -> str:
        return name if name else f"{library} {technique} model"

    @deprecate(
        parameter="inputs",
        warn_at="23.1",
        fail_at="23.2",
        remove_at="23.3",
        reason="The 'inputs' parameter is renamed 'derived_from'. "
        "Using 'inputs' will raise an error in v{fail_at}. "
        "The parameter will be removed in v{remove_at}.",
    )
    def register_model(
        self,
        model: Model,
        project_id: int,
        phase_id: int | None = None,
        iteration_id: int | None = None,
        code_version_id: int | None = None,
        derived_from: list[int] | None = None,
        inputs: list[int] | None = None,
    ) -> ModelRegisterOutput:
        """Register a model.

        Parameters:
            model: The model to register
            project_id: The project ID
            phase_id: The phase ID
            iteration_id: The iteration ID
            code_version_id: The code version ID
            derived_from: The IDs of datasets the model is derived from
            inputs: Deprecated. Use `derived_from` instead

        Returns:
            The registered model.
        """
        if not derived_from and inputs:
            derived_from = inputs

        metrics = [vars(MetricInput(metric.key, metric.value)) for metric in model.metrics] if model.metrics else None
        properties = (
            [vars(PropertyInput(prop.key, prop.value)) for prop in model.properties] if model.properties else None
        )
        model_register_input = ModelRegisterInput(
            name=model.name,
            modelType=ModelType.OTHER.value,
            status=ModelVersionStatus.EXPERIMENTATION.value,
            inputs=derived_from or [],
            metrics=metrics,
            properties=properties,
            algorithmName=model.technique,
            framework=model.library,
            codeVersionId=code_version_id,
        )
        return GqlModelApi(self._gql_client, self.auth).register_model(
            model_register_input, project_id, phase_id, iteration_id
        )

    def get_last_assets(self, target_types: list[str], page):
        return LastAssetApi(self._gql_client, self.auth).get_last_assets(target_types, page)

    def get_user_and_default_workspace(self):
        return UserAndDefaultWorkspaceApi(self._gql_client, self.auth).get_user_and_default_workspace()

    def create_code_gql(self, project_id: int, code: CodeInput):
        return GqlCodeApi(self._gql_client, self.auth).create_code(project_id, code)

    def create_code_version_gql(self, code_id: int, code_version: CodeVersionCreateBody):
        return GqlCodeVersionApi(self._gql_client, self.auth).create_code_version(code_id, code_version)

    def get_code(self, code: str | int, project_id: int | None = None):
        if project_id is None:
            raise MissingReferenceError("project")
        return GqlCodeApi(self._gql_client, self.auth).get_code(code, project_id)

    def get_code_version(self, code_version: str | int, code_id: int | None = None):
        if code_id is None:
            raise MissingReferenceError("code")
        return GqlCodeVersionApi(self._gql_client, self.auth).get_code_version(code_version, code_id)
