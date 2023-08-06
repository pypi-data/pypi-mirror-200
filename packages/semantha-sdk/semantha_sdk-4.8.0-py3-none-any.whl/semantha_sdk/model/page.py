from __future__ import annotations

from dataclasses import dataclass

from marshmallow_dataclass import class_schema
from typing import Optional, List

from semantha_sdk.model.paragraph import Paragraph
from semantha_sdk.model.semantha_entity import SemanthaModelEntity, SemanthaSchema


@dataclass(frozen=True)
class PageContent(SemanthaModelEntity):
    paragraphs: Optional[List[Paragraph]]


PageContentSchema = class_schema(PageContent, base_schema=SemanthaSchema)


@dataclass(frozen=True)
class Page(SemanthaModelEntity):
    contents: List[PageContent]


PageSchema = class_schema(Page, base_schema=SemanthaSchema)
