from __future__ import annotations
from typing import Dict, Any
from modelon.impact.client import exceptions
from modelon.impact.client.entities.workspace import Workspace, WorkspaceDefinition
from modelon.impact.client.operations.base import AsyncOperation, AsyncOperationStatus
from modelon.impact.client.sal.service import Service


class WorkspaceConversionOperation(AsyncOperation):
    """An conversion operation class for the
    modelon.impact.client.entities.workspace.

    Workspace class.

    """

    def __init__(self, location: str, service: Service):
        super().__init__()
        self._location = location
        self._sal = service

    def __repr__(self) -> str:
        return f"Workspace conversion operations for id '{self.id}'"

    def __eq__(self, obj: object) -> bool:
        return (
            isinstance(obj, WorkspaceConversionOperation)
            and obj._location == self._location
        )

    @property
    def id(self) -> str:
        """Workspace conversion id."""
        return self._location.split('/')[-1]

    @property
    def name(self) -> str:
        """Return the name of operation."""
        return "Workspace conversion"

    def _info(self) -> Dict[str, Any]:
        return self._sal.workspace.get_workspace_conversion_status(self._location)[
            "data"
        ]

    def data(self) -> Workspace:
        """Returns a Workspace class instance of the converted workspace.

        Returns:

            An Workspace class instance.

        """
        info = self._info()
        if info['status'] == AsyncOperationStatus.ERROR.value:
            raise exceptions.IllegalWorkspaceConversion(
                f"Workspace conversion failed! Cause: {info['error'].get('message')}"
            )

        workspace_id = info["data"]["workspaceId"]
        resp = self._sal.workspace.workspace_get(workspace_id)
        return Workspace(resp["id"], WorkspaceDefinition(resp["definition"]), self._sal)

    def status(self) -> AsyncOperationStatus:
        """Returns the conversion status as an enumeration.

        Returns:
            The AsyncOperationStatus enum. The status can have the enum values
            AsyncOperationStatus.READY, AsyncOperationStatus.RUNNING or
            AsyncOperationStatus.ERROR

        Example::

            client.convert_workspace(workspace_id).status()

        """
        return AsyncOperationStatus(self._info()["status"])
