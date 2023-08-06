from __future__ import annotations

from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Domain(SemanthaModelEntity):
    id: str
    name: str
    base_url: str


DomainSchema = class_schema(Domain, base_schema=SemanthaSchema)
