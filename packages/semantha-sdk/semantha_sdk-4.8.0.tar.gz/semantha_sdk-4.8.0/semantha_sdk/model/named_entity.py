from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class NamedEntity(SemanthaModelEntity):
    name: str
    text: str


NamedEntitySchema = class_schema(NamedEntity, base_schema=SemanthaSchema)
