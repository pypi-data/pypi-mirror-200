from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.semantha_entity import SemanthaSchema
from semantha_sdk.model.version import Version


@dataclass(frozen=True)
class ProcessInformation(SemanthaModelEntity):
    created: str
    edited: str
    version: Version

ProcessInformationSchema = class_schema(ProcessInformation, base_schema=SemanthaSchema)