# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import doc_content_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_paragraph import NodeParagraph
    from .node_heading import NodeHeading
    from .node_media_single import NodeMediaSingle
    from .node_media_group import NodeMediaGroup
    from .node_code_block import NodeCodeBlock
    from .node_bullet_list import NodeBulletList
    from .node_ordered_list import NodeOrderedList
    from .node_task_list import NodeTaskList
    from .node_decision_list import NodeDecisionList
    from .node_rule import NodeRule
    from .node_panel import NodePanel
    from .node_blockquote import NodeBlockquote
    from .node_extension import NodeExtension


@dataclasses.dataclass(frozen=True)
class NodeNestedExpandAttrs(Base):
    """
    Attributes for :class:`NodeNestedExpand`.

    :param title: Optional. The disclosure label displayed when collapsed.
    :param localId: Optional. A unique identifier for the node.
    """

    title: str = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeNestedExpand(BaseNode):
    """
    A container that allows content to be hidden or shown within table cells.

    The nestedExpand node is similar to an accordion or disclosure widget,
    allowing users to collapse and expand content. Unlike the regular expand
    node, nestedExpand can ONLY be placed within TableCell or TableHeader
    elements - this restriction exists to avoid infinite nesting.

    Common use cases:
    - Hiding detailed information in table cells
    - Creating collapsible sections within complex table layouts
    - Organizing dense tabular content

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/nestedExpand/
    """

    type: str = TypeEnum.nestedExpand.value
    attrs: NodeNestedExpandAttrs = REQ
    content: list[
        T.Union[
            "NodeParagraph",
            "NodeHeading",
            "NodeMediaSingle",
            "NodeMediaGroup",
            "NodeCodeBlock",
            "NodeBulletList",
            "NodeOrderedList",
            "NodeTaskList",
            "NodeDecisionList",
            "NodeRule",
            "NodePanel",
            "NodeBlockquote",
            "NodeExtension",
        ]
    ] = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        """
        .. note::

            We don't preserve expand title in markdown.
        """
        md = doc_content_to_markdown(content=self.content, ignore_error=ignore_error)
        return md
