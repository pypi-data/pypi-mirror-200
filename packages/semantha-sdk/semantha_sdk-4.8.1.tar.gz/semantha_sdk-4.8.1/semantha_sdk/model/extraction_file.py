from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.document import Document
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class ExtractionFile(SemanthaModelEntity):
    id: str
    external_id: str
    name: str
    processed: bool
    binary: str
    document_extractor: str
    document: Document

ExtractionFileSchema = class_schema(ExtractionFile, base_schema=SemanthaSchema)