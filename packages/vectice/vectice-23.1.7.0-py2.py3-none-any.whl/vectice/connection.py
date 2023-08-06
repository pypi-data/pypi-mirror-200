from __future__ import annotations

import logging
import os
from contextlib import suppress
from pathlib import Path
from textwrap import dedent
from typing import TYPE_CHECKING

import dotenv
from rich.table import Table

from vectice.api import Client
from vectice.api.json.last_assets import ActivityTargetType
from vectice.models.workspace import Workspace
from vectice.utils.common_utils import _temp_print, hide_logs
from vectice.utils.configuration import Configuration
from vectice.utils.last_assets import _connection_logging, _get_last_assets, _get_last_user_and_default_workspace
from vectice.utils.logging_utils import CONNECTION_PROJECT_LOGGING, CONNECTION_WORKSPACE_LOGGING, format_description

if TYPE_CHECKING:
    from vectice.models.project import Project


_logger = logging.getLogger(__name__)
DEFAULT_API_ENDPOINT = "https://app.vectice.com"
CAN_NOT_BE_EMPTY_ERROR_MESSAGE = "%s can not be empty."


class Connection:
    """Connect to the Vectice backend (application).

    The Connection class encapsulates a connection to the Vectice App.
    Thus, it authenticates and connects to Vectice.
    This allows you to start interacting with your Vectice assets.

    A Connection can be initialized in three ways:

    1. Passing the relevant arguments to authenticate and connect to Vectice:

        ```python
        import vectice

        connection = vectice.connect(
            api_token="API_TOKEN_FROM_VECTICE",
            host="https://app.vectice.com",
        )
        ```

    2. Passing the path to a configuration file:

        ```python
        import vectice

        connection = vectice.connect(config="vectice_config.json")
        ```

    3. Letting Vectice find the configuration file in specific locations:

        ```python
        import vectice

        connection = vectice.connect()
        ```

    See [`Connection.connect`][vectice.connection.Connection.connect] for more info.
    """

    USER_FILES_PATH = [
        ".vectice",
        str(Path.home() / ".vectice"),
        ".env",
        str(Path.home() / ".env"),
        "/etc/vectice/api.cfg",
    ]

    def __init__(
        self,
        api_token: str,
        host: str,
        workspace: str | int | None = None,
        project: str | int | None = None,
    ):
        """Initialize a connection.

        Parameters:
            api_token: Your private api token.
            host: The address of the Vectice application.
            workspace: The workspace you want to work in.
            project: The project you want to work in.

        Raises:
            RuntimeError: When the API and backend versions are incompatible.
        """
        logging.getLogger("Client").propagate = True
        self._client = Client(
            workspace=workspace,
            project=project,
            token=api_token,
            api_endpoint=host,
            auto_connect=True,
            allow_self_certificate=True,
        )
        compatibility = self._client.check_compatibility()
        if compatibility.status != "OK":
            if compatibility.status == "Error":
                _logger.error(f"compatibility error: {compatibility.message}")
                raise RuntimeError(f"compatibility error: {compatibility.message}")
            else:
                _logger.warning(f"compatibility warning: {compatibility.message}")

    def __repr__(self) -> str:
        return (
            "Connection("
            + f"workspace={self._client.workspace.name if self._client.workspace else 'None'}, "
            + f"host={self._client.auth.api_base_url}, "
        )

    @property
    def version_api(self) -> str:
        return self._client.version_api

    @property
    def version_backend(self) -> str:
        return self._client.version_backend

    def workspace(self, workspace: str | int) -> Workspace:
        """Get a workspace.

        Parameters:
            workspace: The id or the name of the desired workspace.

        Returns:
            The desired workspace.
        """
        output = self._client.get_workspace(workspace)
        result = Workspace(output.id, output.name, output.description)
        result.__post_init__(self._client, self)
        return result

    def list_workspaces(self) -> None:
        """List the workspaces to which this connection has access and log the workspaces in a tabular format.

        Returns:
            The workspaces to which this connection has access.
        """
        workspace_outputs = self._client.list_workspaces().list
        user_name, _ = _get_last_user_and_default_workspace(self._client)

        rich_table = Table(expand=True, show_edge=False)

        rich_table.add_column("workspace id", justify="left", no_wrap=True, min_width=4, max_width=10)
        rich_table.add_column("name", justify="left", no_wrap=True, max_width=20)
        rich_table.add_column("description", justify="left", no_wrap=True, max_width=50)

        for count, workspace in enumerate(workspace_outputs, 1):
            if count > 10:
                break
            rich_table.add_row(str(workspace.id), workspace.name, format_description(workspace.description))

        description = f"""There are {len(workspace_outputs)} workspaces for user {user_name}."""
        tips = dedent(
            """
        >> To access your personal workspace, use connection.my_workspace or connect.workspaces[0]
        >> To access a specific workspace, use connection.workspace(Workspace ID)"""
        ).lstrip()
        link = dedent(
            f"""
        For quick access to the list of workspaces in the Vectice web app, visit:
        {self._client.auth._API_BASE_URL}/workspaces"""
        ).lstrip()
        _temp_print(description)
        _temp_print(table=rich_table)
        _temp_print(tips)
        _temp_print(link)

    @property
    def workspaces(self) -> list[Workspace] | None:
        """List the workspaces to which this connection has access.

        Returns:
            The workspaces to which this connection has access.
        """
        _, default_workspace_id = _get_last_user_and_default_workspace(self._client)
        outputs = self._client.list_workspaces()
        results: list[Workspace] = []
        for output in outputs.list:
            workspace = Workspace(id=output.id, name=output.name, description=output.description)
            workspace.__post_init__(self._client, self)
            if output.id == default_workspace_id:
                results.insert(0, workspace)
                continue
            results.append(workspace)
        return results

    @property
    def my_workspace(self) -> Workspace:
        """Retrieve your personal workspace.

        Returns:
            Personal workspace.
        """
        asset = self._client.get_user_and_default_workspace()
        if not asset.get("defaultWorkspace"):
            raise ValueError("Default workspace is not set.")
        return self.workspace(int(asset["defaultWorkspace"]["id"]))

    @property
    def last_workspace(self) -> Workspace:
        """Retrieve last workspace with activity.

        Returns:
            Last workspace with activity.
        """
        target_types = [activity for activity in ActivityTargetType]
        asset = _get_last_assets(target_types, self._client, _logger)
        if not asset or not asset.get("workspace"):
            raise ValueError("Workspace with activity not found.")
        return self.workspace(int(asset["workspace"]["id"]))

    @staticmethod
    def connect(
        api_token: str | None = None,
        host: str | None = None,
        config: str | None = None,
        workspace: str | int | None = None,
        project: str | None = None,
    ) -> Connection | Workspace | Project | None:
        """Method to connect to the Vectice backend (application).

        Authentication credentials are retrieved, in order, from:

        1. keyword arguments
        2. configuration file (`config` parameter)
        3. environment variables
        4. environment files in the following order
            - `.vectice` of the working directory
            - `.vectice` of the user home directory
            - `.env` of the working directory
            - `.env` of the user home directory
            - `/etc/vectice/api.cfg` file

        This method uses the `api_token`, `host`, `workspace`, `project` arguments
        or the JSON config provided. The JSON config file is available from the Vectice
        webapp when creating an API token.

        Parameters:
            api_token: The api token provided by the Vectice webapp.
            host: The backend host to which the client will connect.
                If not found, the default endpoint https://app.vectice.com is used.
            config: A JSON config file containing keys VECTICE_API_TOKEN and
                VECTICE_API_ENDPOINT as well as optionally WORKSPACE and PROJECT.
            workspace: The name of an optional workspace to return.
            project: The name of an optional project to return.

        Raises:
            ValueError: When a project is specified without a workspace.

        Returns:
            A Connection, Workspace, or Project.
        """
        host = host or Connection._get_host(config)
        api_token = api_token or Connection._get_api_token(host, config)
        workspace = workspace or Connection._get_workspace(config)
        project = project or Connection._get_project(config)
        connection = Connection(api_token=api_token, host=host, workspace=workspace, project=project)
        user_name, workspace_id = _get_last_user_and_default_workspace(connection._client)
        url = connection._client.auth.api_base_url
        if workspace and not project:
            return connection.get_workspace(workspace, user_name, url)
        if workspace and project:
            return connection.get_project(workspace, project, user_name, url)
        _connection_logging(_logger, user_name, url, workspace_id)
        return connection

    @staticmethod
    def _get_host(config: str | None) -> str:
        try:
            return Connection._get_config_item("VECTICE_API_ENDPOINT", config)  # type: ignore[return-value]
        except ValueError:
            _logger.debug(f"No VECTICE_API_ENDPOINT provided. Using default endpoint {DEFAULT_API_ENDPOINT}")
            return DEFAULT_API_ENDPOINT

    @staticmethod
    def _get_api_token(host: str | None, config: str | None) -> str:
        try:
            return Connection._get_config_item("VECTICE_API_TOKEN", config)  # type: ignore[return-value]
        except ValueError as error:
            raise ValueError(
                f"You must provide the api_token. You can generate them by going to the page {host}/account/api-keys"
            ) from error

    @staticmethod
    def _get_workspace(config) -> str | int | None:
        try:
            return Connection._get_config_item("WORKSPACE", config)
        except ValueError:
            return None

    @staticmethod
    def _get_project(config) -> str | None:
        try:
            return str(Connection._get_config_item("PROJECT", config))
        except ValueError:
            return None

    @staticmethod
    def _get_config_item(item_name: str, config_path: str | None) -> str | int:
        # search in provided config file
        with suppress(KeyError, SyntaxError, TypeError):
            config = Configuration(config_path)  # type: ignore[arg-type]
            if config[item_name]:
                _logger.debug(f"Found {item_name} in {config_path}")
                return config[item_name]
        # search in environment variables
        item = os.environ.get(item_name)
        if item:
            _logger.debug(f"Found {item_name} in environment variables.")
            return item
        # search in user configuration files
        for path in Connection.USER_FILES_PATH:
            with hide_logs("dotenv"):
                item = dotenv.get_key(path, item_name)
            if item:
                _logger.debug(f"Found {item_name} in {path}")
                return item
        raise ValueError(f"Could not find {item_name} in user configuration")

    def get_workspace(self, workspace: int | str, user_name: str, host: str) -> Workspace:
        workspace_output: Workspace = self.workspace(workspace)
        _logger.info(
            CONNECTION_WORKSPACE_LOGGING.format(
                user=user_name, workspace_name=workspace_output.name, url=host, workspace_id=workspace_output.id
            )
        )
        return workspace_output

    def get_project(self, workspace: int | str, project: str, user_name: str, host: str) -> Project:
        workspace_output = self.workspace(workspace)
        project_output: Project = workspace_output.project(project)
        _logger.info(
            CONNECTION_PROJECT_LOGGING.format(
                user=user_name,
                project_name=project_output.name,
                url=host,
                workspace_id=workspace_output.id,
                project_id=project_output.id,
            )
        )
        return project_output
