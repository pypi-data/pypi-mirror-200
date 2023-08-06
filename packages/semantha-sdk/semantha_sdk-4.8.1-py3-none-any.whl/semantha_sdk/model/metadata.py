from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Metadata(SemanthaModelEntity):
    id: str
    value: str


MetadataSchema = class_schema(Metadata, base_schema=SemanthaSchema)
