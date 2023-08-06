from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity, Label, Metadata
from semantha_sdk.model.extraction_area import ExtractionArea
from semantha_sdk.model.extraction_reference import ExtractionReference
from semantha_sdk.model.finding import Finding
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class ComplexProperty(SemanthaModelEntity):
    name: str
    value: str
    label: str
    id: str
    class_id: str
    relation_id: str
    original_value: str
    extracted_value: str
    datatype: str
    labels: List[Label]
    metadata: List[Metadata]
    extraction_area: ExtractionArea
    findings: List[Finding]
    references: List[ExtractionReference]

ComplexPropertySchema = class_schema(ComplexProperty, base_schema=SemanthaSchema)