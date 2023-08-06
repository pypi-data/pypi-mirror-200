from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Synonym(SemanthaModelEntity):
    id: str
    word: Optional[str]
    regex: Optional[str]
    synonym: str
    tags: List[str]


SynonymSchema = class_schema(Synonym, base_schema=SemanthaSchema)
