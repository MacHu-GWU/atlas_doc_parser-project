# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import doc_content_to_markdown, add_style_to_markdown

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
class NodeExpandAttrs(Base):
    """
    Attributes for :class:`NodeExpand`.

    :param title: Optional. Display title for the expand container.
    :param localId: Optional. A unique identifier for the node.
    """

    title: str = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeExpand(BaseNode):
    """
    A container that enables content to be hidden or shown.

    The expand node is a top-level block node similar to an accordion or
    disclosure widget. It contains block-level content that can be toggled
    visible or hidden by the user.

    Note: For table cells or headers, use nestedExpand instead of expand.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/expand/
    """

    type: str = TypeEnum.expand.value
    attrs: NodeExpandAttrs = OPT
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
        """
        .. note::

            When converting an expand node to Markdown, any nested expand nodes
            are treated as regular expand nodes without preserving their hierarchical structure.
        """
        md = doc_content_to_markdown(content=self.content, ignore_error=ignore_error)
        md = add_style_to_markdown(md, self)
        return md
