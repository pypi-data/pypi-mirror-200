from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity


@dataclass(frozen=True)
class Finding(SemanthaModelEntity):
    status_code: int
    severity: str
    message: str

FindingSchema = class_schema(Finding)