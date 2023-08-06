from dataclasses import dataclass
from typing import Optional

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class DomainSettings(SemanthaModelEntity):
    similarity_model_id: str
    keep_numbers: bool
    min_tokens: int
    similarity_measure: str
    context_weight: float
    enable_string_comparison: bool
    default_document_type: str
    enable_paragraph_sorting: bool
    enable_paragraph_end_detection: bool
    enable_paragraph_merging_based_on_formatting: bool
    enable_boost_word_filtering_for_input_documents: bool
    enable_no_match_color_red: Optional[bool]
    enable_saturated_match_colors: Optional[bool]
    tagging_similarity_mode: str
    enable_updating_fingerprints_on_tag_updates: bool
    similarity_matcher: str
    similarity_max_deviation: int
    similarity_threshold: float
    enable_tagging: bool
    tagging_threshold: float
    tagging_strategy: str
    extraction_threshold: float
    extraction_strategy: str
    resize_paragraphs_on_extraction: bool
    use_creation_date_from_input_document: bool


DomainSettingsSchema = class_schema(DomainSettings, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class PatchDomainSettings(SemanthaModelEntity):
    similarity_model_id: Optional[str] = None
    keep_numbers: Optional[bool] = None
    min_tokens: Optional[int] = None
    similarity_measure: Optional[str] = None
    context_weight: Optional[float] = None
    enable_string_comparison: Optional[bool] = None
    default_document_type: Optional[str] = None
    enable_paragraph_sorting: Optional[bool] = None
    enable_paragraph_end_detection: Optional[bool] = None
    enable_paragraph_merging_based_on_formatting: Optional[bool] = None
    enable_boost_word_filtering_for_input_documents: Optional[bool] = None
    tagging_similarity_mode: Optional[str] = None
    enable_updating_fingerprints_on_tag_updates: Optional[bool] = None
    similarity_matcher: Optional[str] = None
    similarity_max_deviation: Optional[int] = None
    similarity_threshold: Optional[float] = None
    enable_tagging: Optional[bool] = None
    tagging_threshold: Optional[float] = None
    tagging_strategy: Optional[str] = None
    extraction_threshold: Optional[float] = None
    extraction_strategy: Optional[str] = None
    resize_paragraphs_on_extraction: Optional[bool] = None
    use_creation_date_from_input_document: Optional[bool] = None
