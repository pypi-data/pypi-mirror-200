from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class DocumentMetadata(SemanthaModelEntity):
    file_name: str
    document_type: str


DocumentMetadataSchema = class_schema(DocumentMetadata, base_schema=SemanthaSchema)
