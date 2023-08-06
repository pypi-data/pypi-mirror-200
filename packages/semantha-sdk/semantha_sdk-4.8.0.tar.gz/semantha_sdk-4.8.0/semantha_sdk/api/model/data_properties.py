from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint


class DataPropertiesEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/dataproperties"

    def get(self, domain: str):
        """ (Not yet implemented) """
        raise NotImplementedError("Not  yet implemented!")
        return self._session.get(f"/api/domains/{domain.lower()}/dataproperties").execute()

    def post(self, domain: str, body: dict):
        """ (Not yet implemented) """
        raise NotImplementedError("Not  yet implemented!")
        return self._session.post(f"/api/domains/{domain.lower()}/dataproperties", ).execute()
