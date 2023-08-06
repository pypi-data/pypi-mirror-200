from __future__ import annotations

from dataclasses import dataclass

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class VersionInfo(SemanthaModelEntity):
    title: str
    vendor: str
    time: str
    version: str
    git: str


VersionInfoSchema = class_schema(VersionInfo, base_schema=SemanthaSchema)
