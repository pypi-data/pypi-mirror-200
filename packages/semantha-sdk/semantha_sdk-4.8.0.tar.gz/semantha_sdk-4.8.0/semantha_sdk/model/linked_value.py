from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class LinkedValue(SemanthaModelEntity):
    value: str
    linked_value: str

LinkedValueSchema = class_schema(LinkedValue, base_schema=SemanthaSchema)