from __future__ import annotations

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.reference_document import ReferenceDocumentsSchema


class DomainTagEndpoint(SemanthaAPIEndpoint):
    def __init__(self, session, endpoint, tag: str):
        SemanthaAPIEndpoint.__init__(self, session, endpoint)
        self.tag = tag

    @property
    def _endpoint(self):
        return f"{self._parent_endpoint}/{self.tag}"

    @property
    def referencedocuments(self):
        class ReferenceDocumentsForTag(SemanthaAPIEndpoint):
            @property
            def _endpoint(self):
                return f"{self._parent_endpoint}/referencedocuments"

            def get(self):
                return self._session.get(self._endpoint).execute().as_list()

            def delete(self):
                return self._session.delete(self._endpoint)

        return ReferenceDocumentsForTag(self._session, self._endpoint)

class DomainTagsEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/tags"

    def get(self) -> list[str]:
        """Get all tags that are defined for the domain"""
        return self._session.get(self._endpoint).execute().as_list()

    def __call__(self, tag: str):
        return DomainTagEndpoint(self._session, self._endpoint, tag)