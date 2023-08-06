from __future__ import annotations

from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import class_schema

from semantha_sdk.model.data_type import DataType
from semantha_sdk.model.label import Label
from semantha_sdk.model.metadata import Metadata
from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Class(SemanthaModelEntity):
    id: str
    name: str
    read_only: bool
    functional: bool
    labels: List[Label]
    metadata: List[Metadata]
    comment: str
    datatype: DataType
    attribute_ids: List[str]
    relevant_for_relation: bool
    object_property_id: str
    parent_id: str


ClassSchema = class_schema(Class, base_schema=SemanthaSchema)
