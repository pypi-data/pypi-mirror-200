from __future__ import annotations

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.user_data import UserData, UserDataSchema
from semantha_sdk.rest.rest_client import RestClient


class CurrentUserRolesEndpoint(SemanthaAPIEndpoint):
    """ Access role(s) information about the currently logged-in user. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/roles"

    def get(self) -> list[str]:
        return self._session.get(self._endpoint).execute().as_list()


class CurrentUserEndpoint(SemanthaAPIEndpoint):
    """ Access information about the currently logged-in user. """

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__roles = CurrentUserRolesEndpoint(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/currentuser"

    @property
    def roles(self):
        return self.__roles

    def get(self) -> UserData:
        return self._session.get(self._endpoint).execute().to(UserDataSchema)
