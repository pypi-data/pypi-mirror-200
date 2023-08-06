from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from marshmallow_dataclass import class_schema

from semantha_sdk.model.entity import Entity
from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class Parameters(SemanthaModelEntity):
    domain: str
    limit: Optional[int]
    offset: Optional[int]
    sort_by: Optional[str] = field(metadata=dict(data_key="sort"))
    return_fields: Optional[str] = field(metadata=dict(data_key="fields"))
    filter_document_ids: Optional[str] = field(metadata=dict(data_key="documentids"))
    filter_tags: Optional[str] = field(metadata=dict(data_key="tags"))
    filter_document_class_ids: Optional[str] = field(metadata=dict(data_key="documentclassids"))
    filter_name: Optional[str] = field(metadata=dict(data_key="name"))
    filter_created_before: Optional[int] = field(metadata=dict(data_key="createdbefore"))
    filter_created_after: Optional[int] = field(metadata=dict(data_key="createdafter"))
    filter_metadata: Optional[str] = field(metadata=dict(data_key="metadata"))
    filter_comment: Optional[str] = field(metadata=dict(data_key="comment"))


ParametersSchema = class_schema(Parameters, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class MetaInfoPage(SemanthaModelEntity):
    range_from: int = field(metadata=dict(data_key="from"))
    range_to: int = field(metadata=dict(data_key="to"))
    range_total: int = field(metadata=dict(data_key="total"))


MetaInfoPageSchema = class_schema(MetaInfoPage, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class Meta(SemanthaModelEntity):
    parameters: Parameters
    info: Optional[str]
    warnings: Optional[List[str]]
    page: Optional[MetaInfoPage]


MetaSchema = class_schema(Meta, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class DocumentInformation(SemanthaModelEntity):
    id: Optional[str] = None
    name: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[str] = None
    filename: Optional[str] = None
    created: Optional[int] = None
    updated: Optional[int] = None
    processed: Optional[bool] = None
    lang: Optional[str] = None
    content: Optional[str] = None
    document_class: Optional[Entity] = None
    derived_tags: List[str] = None
    color: Optional[str] = None
    derived_color: Optional[str] = None
    comment: Optional[str] = None
    derived_comment: Optional[str] = None
    content_preview: Optional[str] = None


DocumentInformationSchema = class_schema(DocumentInformation, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class DocsPerTag(SemanthaModelEntity):
    tag: str
    count: int


DocsPerTagSchema = class_schema(DocsPerTag, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class Statistics(SemanthaModelEntity):
    library_size: int
    size: int
    number_of_sentences: int
    docs_per_tag: List[DocsPerTag]


StatisticsSchema = class_schema(Statistics, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class ReferenceDocuments(SemanthaModelEntity):
    meta: Meta
    documents: Optional[List[DocumentInformation]] = field(default_factory=list, metadata=dict(data_key="data"))


ReferenceDocumentsSchema = class_schema(ReferenceDocuments, base_schema=SemanthaSchema)
