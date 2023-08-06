from __future__ import annotations

import logging
from textwrap import dedent
from typing import TYPE_CHECKING

from rich.table import Table

from vectice.api.json.iteration import IterationStatus
from vectice.models.phase import Phase
from vectice.models.resource import Resource
from vectice.utils.common_utils import _temp_print
from vectice.utils.deprecation import DeprecationError
from vectice.utils.last_assets import _get_last_user_and_default_workspace
from vectice.utils.logging_utils import get_phase_status

if TYPE_CHECKING:
    from vectice import Connection
    from vectice.models import Workspace


_logger = logging.getLogger(__name__)


class Project:
    """Represent a Vectice project.

    A project reflects a typical Data Science project, including
    phases and the associated assets like code, datasets, models, and
    documentation. Multiple projects may be defined within each workspace.

    You can get a project from your [`Workspace`][vectice.models.Workspace]
    object by calling `project()`:

    ```python
    import vectice

    connection = vectice.connect(...)
    my_workspace = connection.workspace("Iris workspace")
    my_project = my_workspace.project("Iris project")
    ```

    Or you can get it directly when connecting to Vectice:

    ```python
    import vectice

    my_project = vectice.connect(..., workspace="Iris workspace", project="Iris project")
    ```

    See [`Connection.connect`][vectice.Connection.connect] to learn
    how to connect to Vectice.
    """

    __slots__ = ["_id", "_workspace", "_name", "_description", "_phase", "_client", "_pointers"]

    def __init__(
        self,
        id: int,
        workspace: Workspace,
        name: str,
        description: str | None = None,
    ):
        """Initialize a project.

        Vectice users shouldn't need to instantiate Projects manually,
        but here are the project parameters.

        Parameters:
            id: The project identifier.
            workspace: The workspace this project belongs to.
            name: The name of the project.
            description: A brief description of the project.
        """
        self._id = id
        self._workspace = workspace
        self._name = name
        self._description = description
        self._phase: Phase | None = None
        self._client = workspace._client

    def __repr__(self):
        description = self._description if self._description else "None"
        return f"Project(name={self.name!r}, id={self._id}, description={description!r}, workspace={self._workspace!r})"

    def __eq__(self, other: object):
        if not isinstance(other, Project):
            return NotImplemented
        return self.id == other.id

    @property
    def id(self) -> int:
        """The project's id.

        Returns:
            The project's id.
        """
        return self._id

    @property
    def workspace(self) -> Workspace:
        """The workspace to which this project belongs.

        Returns:
            The workspace to which this project belongs.
        """
        return self._workspace

    @property
    def connection(self) -> Connection:
        """The Connection to which this project belongs.

        Returns:
            The Connection to which this project belongs.
        """
        return self._workspace.connection

    @property
    def name(self) -> str:
        """The project's name.

        Returns:
            The project's name.
        """
        return self._name

    @property
    def description(self) -> str | None:
        """The project's description.

        Returns:
            The project's description.
        """
        return self._description

    @property
    def properties(self) -> dict:
        """The project's identifiers.

        Returns:
            A dictionary containing the `name`, `id` and `workspace` items.
        """
        return {"name": self.name, "id": self.id, "workspace": self.workspace.id}

    @property
    def origin_dataset(self) -> None:
        """Deprecated. Use steps' [`origin_dataset`][vectice.models.Step.origin_dataset] instead.

        Raises:
            DeprecationError: Always.
        """
        raise DeprecationError("Origin datasets are now set in steps.")

    @origin_dataset.setter
    def origin_dataset(self, data_source: Resource) -> None:
        """Deprecated. Use steps' [`origin_dataset`][vectice.models.Step.origin_dataset] instead.

        Parameters:
            data_source: The origin dataset.

        Raises:
            DeprecationError: Always.
        """
        raise DeprecationError("Origin datasets are now set in steps.")

    def phase(self, phase: str | int) -> Phase:
        """Get a phase.

        Parameters:
            phase: The name or id of the phase to get.

        Returns:
            The specified phase.
        """
        item = self._client.get_phase(phase, project_id=self._id)
        _logger.debug(f"Phase with id: {item.id} successfully retrieved.")
        phase_object = Phase(item.id, self, item.name, item.index, item.status)
        self._phase = phase_object
        return phase_object

    def list_phases(self) -> None:
        """List the phases to which this project has access and print the phases in a tabular format.

        Returns:
            None
        """
        phase_outputs = sorted(self._client.list_phases(project=self.id), key=lambda x: x.index)
        user_name, _ = _get_last_user_and_default_workspace(self._client)

        rich_table = Table(expand=True, show_edge=False)

        rich_table.add_column("phase id", justify="left", no_wrap=True, min_width=3, max_width=5)
        rich_table.add_column("name", justify="left", no_wrap=True, min_width=5, max_width=10)
        rich_table.add_column("owner", justify="left", no_wrap=True, min_width=4, max_width=4)
        rich_table.add_column("status", justify="left", no_wrap=True, min_width=4, max_width=4)
        rich_table.add_column("iterations", justify="left", no_wrap=True, min_width=4, max_width=4)
        rich_table.add_column("steps", justify="left", no_wrap=True, max_width=10)

        for count, phase in enumerate(phase_outputs, 1):
            if count > 10:
                break
            phase_iterations = self._client.list_iterations(phase.id)
            iterations_total = len(phase_iterations)
            active_iterations = len(
                [
                    iteration
                    for iteration in phase_iterations
                    if iteration.status is not (IterationStatus.Completed or IterationStatus.Abandoned)
                ]
            )
            phase_owner = phase["owner"]["name"] if phase.get("owner") else "Unassigned"
            phase_status = get_phase_status(phase.status)
            phase_steps = self._client.list_step_definitions(phase.id)
            total_phase_steps = len(phase_steps)
            rich_table.add_row(
                str(phase.id),
                phase.name,
                phase_owner,
                phase_status,
                f"{active_iterations}/{iterations_total}",
                str(total_phase_steps),
            )
        description = f"""There are {len(phase_outputs)} phases in the project {self.name} for user {user_name}."""
        tips = dedent(
            """
        >> To access a specific phase, use project.phase(PhaseID)
        >> To access an array of phases, use project.phases"""
        ).lstrip()
        link = dedent(
            f"""
        For quick access to the list of phases for this project, visit:
        {self._client.auth._API_BASE_URL}/project?w={self.workspace.id}&resourceId={self.id}"""
        ).lstrip()
        legend = """**Legend**     [C]  Completed     [IP] In Progress
               [IR] In Review     [NS] Not Started"""

        _temp_print(description)
        _temp_print(legend)
        _temp_print(table=rich_table)
        _temp_print(tips)
        _temp_print(link)

    @property
    def phases(self) -> list[Phase]:
        """The project's phases.

        Returns:
            The phases associated with this project.
        """
        outputs = self._client.list_phases(project=self._id)
        return sorted(
            [Phase(item.id, self, item.name, item.index, item.status) for item in outputs], key=lambda x: x.index
        )
