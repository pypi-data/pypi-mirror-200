from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger

    from vectice.api import Client
    from vectice.api.json.last_assets import ActivityTargetType


def _get_last_assets(target_types: list[ActivityTargetType], client: Client, _logger: Logger):
    target_types_array = [target.value for target in target_types]
    try:
        last_asset = client.get_last_assets(target_types_array, {"index": 1, "size": 1}).list[0]
        return last_asset
    except IndexError as e:
        _logger.debug(f"There were no assets with activity found. Sanity check {e}")
        return


def _get_last_user_and_default_workspace(client: Client) -> tuple[str, int | None]:
    asset = client.get_user_and_default_workspace()
    workspace_id = int(asset["defaultWorkspace"]["id"]) if asset["defaultWorkspace"] else None
    return asset["user"]["name"], workspace_id


def _connection_logging(_logger: Logger, user_name: str, host: str, workspace_id: int | None):
    from vectice.utils.logging_utils import CONNECTION_LOGGING

    if workspace_id:
        CONNECTION_LOGGING += r"/workspace/dashboard?w={workspace_id}"  # noqa: N806
        _logger.info(CONNECTION_LOGGING.format(user=user_name, url=host, workspace_id=workspace_id))
        return
    CONNECTION_LOGGING += r"/workspaces"  # noqa: N806
    _logger.info(CONNECTION_LOGGING.format(user=user_name, url=host))
