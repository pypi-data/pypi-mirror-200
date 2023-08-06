from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.linked_value import LinkedValue
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class LinkedInstance(SemanthaModelEntity):
    instance_id: str
    linked_values: List[LinkedValue]


LinkedInstanceSchema = class_schema(LinkedInstance, base_schema=SemanthaSchema)