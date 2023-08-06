from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint


class MetadataTypesEndpoint(SemanthaAPIEndpoint):
    """ api/model/metadatatypes endpoint. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/metadatatypes"

    def get(self):
        pass
