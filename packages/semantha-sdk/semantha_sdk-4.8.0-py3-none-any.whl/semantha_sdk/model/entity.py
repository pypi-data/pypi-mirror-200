from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Entity(SemanthaModelEntity):
    id: str
    name: str


EntitySchema = class_schema(Entity, base_schema=SemanthaSchema)
