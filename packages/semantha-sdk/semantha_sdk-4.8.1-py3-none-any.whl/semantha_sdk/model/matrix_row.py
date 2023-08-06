from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity, Reference
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class MatrixRow(SemanthaModelEntity):
    document_id: str
    document_name: str
    references: List[Reference]


MatrixRowSchema = class_schema(MatrixRow, base_schema=SemanthaSchema)