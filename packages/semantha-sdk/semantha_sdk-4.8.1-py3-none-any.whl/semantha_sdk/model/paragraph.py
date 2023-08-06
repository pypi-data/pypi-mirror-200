from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Dict

from marshmallow_dataclass import class_schema

from semantha_sdk.model.reference import Reference
from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema
from semantha_sdk.model.sentence import Sentence
from semantha_sdk.model.area import Area


@dataclass(frozen=True)
class Paragraph(SemanthaModelEntity):
    id: str
    type: str
    text: str
    sentences: Optional[List[Sentence]]
    document_name: Optional[str]
    areas: Optional[List[Area]]
    references: Optional[List[Reference]]
    context: Optional[Dict[str, str]]
    comment: Optional[str]


ParagraphSchema = class_schema(Paragraph, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class PatchParagraph(SemanthaModelEntity):
    id: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    sentences: Optional[List[Sentence]] = None
    document_name: Optional[Optional[str]] = None
    references: Optional[List[Reference]] = None
    context: Optional[Dict[str, str]] = None
    comment: Optional[str] = None
