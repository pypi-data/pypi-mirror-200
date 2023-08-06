from dataclasses import dataclass
from typing import Any

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class ModelClass:
    name: str
    label: str
    # TODO: is this nested?
    sub_model_classes: Any

ModelClassSchema = class_schema(ModelClass, base_schema=SemanthaSchema)