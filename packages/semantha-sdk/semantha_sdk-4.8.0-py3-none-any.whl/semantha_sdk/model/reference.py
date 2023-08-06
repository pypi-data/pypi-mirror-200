from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Reference(SemanthaModelEntity):
    document_id: str
    similarity: float
    color: Optional[str]
    document_name: Optional[str]
    page_number: Optional[int]
    paragraph_id: Optional[str]
    sentence_id: Optional[str]
    text: Optional[str]
    context: Optional[Dict[str, str]]
    type: Optional[str]
    comment: Optional[str]
    has_opposite_meaning: Optional[bool]


ReferenceSchema = class_schema(Reference, base_schema=SemanthaSchema)
