# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import doc_content_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_paragraph import NodeParagraph
    from .node_panel import NodePanel
    from .node_blockquote import NodeBlockquote
    from .node_ordered_list import NodeOrderedList
    from .node_bullet_list import NodeBulletList
    from .node_rule import NodeRule
    from .node_heading import NodeHeading
    from .node_code_block import NodeCodeBlock
    from .node_media_group import NodeMediaGroup
    from .node_media_single import NodeMediaSingle
    from .node_decision_list import NodeDecisionList
    from .node_task_list import NodeTaskList
    from .node_table import NodeTable
    from .node_block_card import NodeBlockCard
    from .node_embed_card import NodeEmbedCard
    from .node_extension import NodeExtension
    from .node_nested_expand import NodeNestedExpand


@dataclasses.dataclass(frozen=True)
class NodeLayoutColumnAttrs(Base):
    """
    Attributes for :class:`NodeLayoutColumn`.

    :param width: Optional. Column width as a percentage (e.g., 50.0 for 50%).
    """

    width: float = OPT


@dataclasses.dataclass(frozen=True)
class NodeLayoutColumn(BaseNode):
    """
    A column within a layout section containing block-level content.

    Layout columns appear exclusively as children of :class:`NodeLayoutSection`.
    Each column can have an optional width attribute (percentage) and contains
    block-level content similar to other container nodes.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/layoutColumn/
    """

    type: str = TypeEnum.layoutColumn.value
    attrs: NodeLayoutColumnAttrs = OPT
    content: list[
        T.Union[
            "NodeParagraph",
            "NodePanel",
            "NodeBlockquote",
            "NodeOrderedList",
            "NodeBulletList",
            "NodeRule",
            "NodeHeading",
            "NodeCodeBlock",
            "NodeMediaGroup",
            "NodeMediaSingle",
            "NodeDecisionList",
            "NodeTaskList",
            "NodeTable",
            "NodeBlockCard",
            "NodeEmbedCard",
            "NodeExtension",
            "NodeNestedExpand",
        ]
    ] = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return doc_content_to_markdown(content=self.content, ignore_error=ignore_error)
