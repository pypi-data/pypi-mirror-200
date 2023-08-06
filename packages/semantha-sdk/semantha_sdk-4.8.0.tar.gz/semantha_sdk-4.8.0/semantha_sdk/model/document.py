from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from marshmallow_dataclass import class_schema

from semantha_sdk.model.page import Page
from semantha_sdk.model.reference import Reference
from semantha_sdk.model.reference_document import DocumentInformation
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class Document(DocumentInformation):
    pages: Optional[List[Page]] = None
    references: Optional[List[Reference]] = None
    image_pages: Optional[str] = None

    def __hash__(self):
        return hash(self.id)


DocumentSchema = class_schema(Document, base_schema=SemanthaSchema)
