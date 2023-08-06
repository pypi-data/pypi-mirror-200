from __future__ import annotations

from typing import Optional

from semantha_sdk.api.semantha_endpoint import SemanthaAPIEndpoint
from semantha_sdk.model.named_entity import NamedEntity, NamedEntitySchema


class NamedEntitiesEndpoint(SemanthaAPIEndpoint):

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/namedentities"

    def get(self) -> Optional[list[NamedEntity]]:
        """ Get all named entities (aka custom entities) that were extracted from the reference documents.
        Note: Might be None iff no named entities have been extracted.
        """
        res = self._session.get(self._endpoint).execute()
        if res.content_is_empty():
            return None
        return self._session.get(self._endpoint).execute().to(NamedEntitySchema)
