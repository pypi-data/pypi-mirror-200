from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema
from typing import Optional

@dataclass(frozen=True)
class Area(SemanthaModelEntity):
    x: float
    y: float
    width: float
    height: float
    page: Optional[int]


AreaSchema = class_schema(Area, base_schema=SemanthaSchema)
