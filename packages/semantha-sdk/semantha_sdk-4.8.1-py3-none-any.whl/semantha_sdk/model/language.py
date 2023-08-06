from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.semantha_entity import SemanthaSchema


@dataclass(frozen=True)
class Language(SemanthaModelEntity):
    language: str

LanguageSchema = class_schema(Language, base_schema=SemanthaSchema)