from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class SimpleProperty(SemanthaModelEntity):
    name: str
    value: str
    property_id: str


SimplePropertySchema = class_schema(SimpleProperty, base_schema=SemanthaSchema)