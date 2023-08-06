from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class Rect(SemanthaModelEntity):
    x: float
    y: float
    width: float
    height: float
    page: int

RectSchema = class_schema(Rect, base_schema=SemanthaSchema)