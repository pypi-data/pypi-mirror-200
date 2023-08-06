from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Label(SemanthaModelEntity):
    lang: str
    value: str


LabelSchema = class_schema(Label, base_schema=SemanthaSchema)
