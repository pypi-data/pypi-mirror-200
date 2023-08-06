from __future__ import annotations

import logging
import logging.config
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vectice.api.json.phase import PhaseStatus


CONNECTION_LOGGING = """Welcome, {user}. You`re now successfully connected to Vectice.

To access your personal workspace, use connection.my_workspace or connection.workspaces[0]
To access a specific workspace, use connection.workspace(Workspace ID)
To get a list of workspaces you can access and their IDs, use connection.list_workspaces()

If you are using a notebook you can call the help by using a Vectice returned object with the builtin notebook "?":
>> connection?

If you are using an IDE you can call the help() method on any object returned by Vectice:
>> help(connection)

For quick access to the list of workspaces in the Vectice web app, visit:
{url}"""

CONNECTION_WORKSPACE_LOGGING = """Welcome, {user}. You`re now successfully connected to the workspace {workspace_name} in Vectice.

To access a specific project, use workspace.project(Project ID)
To get a list of projects you can access and their IDs, use workspace.list_projects()

For quick access to the list of projects in the Vectice web app, visit:
{url}/workspace/projects?w={workspace_id}"""

CONNECTION_PROJECT_LOGGING = """Welcome, {user}. You`re now successfully connected to the project {project_name} in Vectice.

To access a specific phase, use project.phase(Phase ID)
To get a list of phases you can access and their IDs, use project.list_phases()

For quick access to the list of phases in the Vectice web app, visit:
{url}/project?w={workspace_id}&resourceId={project_id}"""


class VecticeLoggingStream:
    """A Python stream for use with event logging APIs throughout vectice (`logger.info()`, etc.).

    This stream wraps `sys.stderr`, forwarding `write()`
    and `flush()` calls to the stream referred to by `sys.stderr` at the time of the call.
    It also provides capabilities for disabling the stream to silence event logs and
    enable propagation for pytest.
    """

    def __init__(self):
        self._enabled = True

    def write(self, text):
        if self._enabled:
            sys.stderr.write(text)

    def flush(self):
        if self._enabled:
            sys.stderr.flush()

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value


VECTICE_LOGGING_STREAM = VecticeLoggingStream()


def disable_logging():
    """Disable logging.

    Disable the `VecticeLoggingStream` used by event logging APIs throughout Vectice
    `logger.info()` silencing all subsequent event logs.
    """
    VECTICE_LOGGING_STREAM.enabled = False


def enable_logging():
    """Enable logging.

    Enable the `VecticeLoggingStream` used by event logging APIs throughout Vectice.
    This reverses the effects of `disable_logging()`.
    """
    VECTICE_LOGGING_STREAM.enabled = True


def enable_propagation():
    """Enable propagation.

    Enable the `VecticeLoggingStream` propagation used by event logging APIs throughout Vectice.
    The testing suite can use caplog to test the logging stdout.
    """
    _configure_vectice_loggers("vectice", propagate=True)


def _configure_vectice_loggers(root_module_name, propagate=False):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "vectice_formatter": {
                    "format": None,
                    "datefmt": None,
                },
            },
            "handlers": {
                "vectice_handler": {
                    "formatter": "vectice_formatter",
                    "class": "logging.StreamHandler",
                    "stream": VECTICE_LOGGING_STREAM,
                },
            },
            "loggers": {
                root_module_name: {
                    "handlers": ["vectice_handler"],
                    "level": "INFO",
                    "propagate": propagate,
                },
            },
        }
    )


def format_description(description: str | None) -> str | None:
    if not description:
        return None
    return description


def get_phase_status(status: PhaseStatus) -> str:
    from vectice.api.json.phase import PhaseStatus

    if status is PhaseStatus.Completed:
        return "[C]"
    if status is PhaseStatus.NotStarted:
        return "[NS]"
    if status is PhaseStatus.InProgress:
        return "[IP]"
    if status is PhaseStatus.InReview:
        return "[IR]"
    return "UK"
