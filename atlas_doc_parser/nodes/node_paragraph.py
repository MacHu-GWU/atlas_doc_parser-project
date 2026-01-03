# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode, BaseMark
from ..markdown_helpers import content_to_markdown, add_style_to_markdown


@dataclasses.dataclass(frozen=True)
class NodeParagraphAttrs(Base):
    """
    Attributes for :class:`NodeParagraph`.

    :param localId: Optional. A unique identifier for the node.
    """

    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeParagraph(BaseNode):
    """
    A container for a block of formatted text delineated by a carriage return.

    The paragraph node is a top-level block node equivalent to HTML's ``<p>`` tag.
    It contains inline nodes such as text, mentions, emojis, and other inline elements.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/paragraph/
    """

    type: str = TypeEnum.paragraph.value
    attrs: NodeParagraphAttrs = OPT
    content: list[BaseNode] = OPT
    marks: list[BaseMark] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        md = content_to_markdown(
            content=self.content,
            ignore_error=ignore_error,
        )
        md = add_style_to_markdown(md, self)
        return md + "\n"
