from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint


class ExtractorTypesEndpoint(SemanthaAPIEndpoint):
    """ api/model/extractortypes endpoint. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/extractortypes"

    def get(self):
        pass