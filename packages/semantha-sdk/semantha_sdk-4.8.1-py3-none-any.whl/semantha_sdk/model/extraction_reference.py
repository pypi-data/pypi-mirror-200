from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class ExtractionReference(SemanthaModelEntity):
    document_id: str
    similarity: float
    used: bool

ExtractionReferenceSchema = class_schema(ExtractionReference, base_schema=SemanthaSchema)