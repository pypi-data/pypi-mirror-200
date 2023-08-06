from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.extraction_file import ExtractionFile
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class FileReference(SemanthaModelEntity):
    file_id: str
    name: str
    page_number: int

FileReferenceSchema = class_schema(FileReference, base_schema=SemanthaSchema)