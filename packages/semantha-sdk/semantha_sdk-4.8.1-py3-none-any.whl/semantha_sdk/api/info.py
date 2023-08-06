from __future__ import annotations

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.info import VersionInfo as VersionInfo, VersionInfoSchema


class InfoEndpoint(SemanthaAPIEndpoint):
    """ Returns API version information. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/info"

    def get(self) -> VersionInfo:
        """ 
        """

        return self._session.get(self._endpoint).execute().to(VersionInfoSchema)
