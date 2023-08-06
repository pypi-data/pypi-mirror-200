from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema
from marshmallow_dataclass import class_schema


@dataclass(frozen=True)
class Boostword(SemanthaModelEntity):
    id: str
    word: Optional[str]
    regex: Optional[str]
    tags: List[str]


BoostwordSchema = class_schema(Boostword, base_schema=SemanthaSchema)
