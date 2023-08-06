from dataclasses import dataclass
from typing import Any, List

from marshmallow_dataclass import class_schema

from semantha_sdk.model import SemanthaModelEntity
from semantha_sdk.model.extraction_file import ExtractionFile
from semantha_sdk.model.model_instance import ModelInstance
from semantha_sdk.model.process_information import ProcessInformation
from semantha_sdk.model.semantha_entity import SemanthaSchema
from semantha_sdk.model.table_instance import TableInstance


@dataclass(frozen=True)
class SemanticModel(SemanthaModelEntity):
    files: List[ExtractionFile]
    instances: List[ModelInstance]
    tables: List[TableInstance]
    process_information: ProcessInformation


SemanticModelSchema = class_schema(SemanticModel, base_schema=SemanthaSchema)