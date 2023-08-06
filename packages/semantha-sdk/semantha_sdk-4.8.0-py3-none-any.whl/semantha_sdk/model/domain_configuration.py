from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.domain_settings import DomainSettings
from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class DomainConfiguration(SemanthaModelEntity):
    id: str
    name: str
    settings: DomainSettings


DomainConfigurationSchema = class_schema(DomainConfiguration, base_schema=SemanthaSchema)
