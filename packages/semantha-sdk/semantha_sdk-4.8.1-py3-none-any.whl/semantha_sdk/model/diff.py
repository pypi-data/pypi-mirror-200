from __future__ import annotations

from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Diff(SemanthaModelEntity):
    operation: str
    text: str


DiffSchema = class_schema(Diff, base_schema=SemanthaSchema)
