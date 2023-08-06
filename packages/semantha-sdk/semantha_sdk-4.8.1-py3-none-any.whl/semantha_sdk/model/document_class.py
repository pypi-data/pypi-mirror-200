from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class DocumentClass(SemanthaModelEntity):
    id: str
    name: str
    created: Optional[int] = None
    updated: Optional[int] = None
    documents_count: int = None
    parent_id: Optional[str] = None
    sub_classes: Optional[List[DocumentClass]] = None
    tags: Optional[List[str]] = None
    derived_tags: Optional[List[str]] = None
    color: Optional[str] = None
    comment: Optional[str] = None
    derived_comment: Optional[str] = None
    metadata: Optional[str] = None
    derived_metadata: Optional[str] = None


@dataclass(frozen=True)
class CreateDocumentClass(SemanthaModelEntity):
    name: str
    color: str
    tags: List[str]
    comment: str
    metadata: str


DocumentClassSchema = class_schema(DocumentClass, base_schema=SemanthaSchema)
