from __future__ import annotations

from dataclasses import dataclass
from typing import List

from marshmallow_dataclass import class_schema

from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class ClusteredDocument(SemanthaModelEntity):
    document_id: str
    probability: float


ClusteredDocumentSchema = class_schema(ClusteredDocument, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class ClusteredParagraph(SemanthaModelEntity):
    document_id: str
    paragraph_id: str
    probability: float


ClusteredParagraphSchema = class_schema(ClusteredParagraph, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class DocumentCluster(SemanthaModelEntity):
    id: int
    count: int
    label: str
    content: List[ClusteredDocument]


DocumentClusterSchema = class_schema(DocumentCluster, base_schema=SemanthaSchema)

@dataclass(frozen=True)
class ClusterDocumentsResponse(SemanthaModelEntity):
    clusters: List[DocumentCluster]
    plotly: dict

ClusterDocumentsResponseSchema = class_schema(ClusterDocumentsResponse, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class ParagraphCluster(SemanthaModelEntity):
    id: int
    count: int
    label: str
    content: List[ClusteredParagraph]


ParagraphClusterSchema = class_schema(ParagraphCluster, base_schema=SemanthaSchema)
