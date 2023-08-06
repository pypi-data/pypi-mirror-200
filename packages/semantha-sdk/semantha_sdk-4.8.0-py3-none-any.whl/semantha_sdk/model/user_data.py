from __future__ import annotations

from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class UserData(SemanthaModelEntity):
    name: str
    valid_until: int
    roles: List[str]


UserDataSchema = class_schema(UserData, base_schema=SemanthaSchema)
