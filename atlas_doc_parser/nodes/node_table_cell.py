# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import content_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_paragraph import NodeParagraph
    from .node_panel import NodePanel
    from .node_blockquote import NodeBlockquote
    from .node_ordered_list import NodeOrderedList
    from .node_bullet_list import NodeBulletList
    from .node_rule import NodeRule
    from .node_heading import NodeHeading
    from .node_code_block import NodeCodeBlock
    from .node_media_single import NodeMediaSingle
    from .node_media_group import NodeMediaGroup
    from .node_decision_list import NodeDecisionList
    from .node_task_list import NodeTaskList
    from .node_block_card import NodeBlockCard
    from .node_embed_card import NodeEmbedCard
    from .node_extension import NodeExtension
    from .node_nested_expand import NodeNestedExpand


@dataclasses.dataclass(frozen=True)
class NodeTableCellAttrs(Base):
    """
    Attributes for :class:`NodeTableCell`.

    :param colspan: Optional. Number of columns this cell spans (defaults to 1).
    :param rowspan: Optional. Number of rows this cell spans (defaults to 1).
    :param colwidth: Optional. Array of column widths in pixels; use 0 for unfixed columns.
    :param background: Optional. Cell background color (hex codes or HTML color names).
    :param localId: Optional. A unique identifier for the node.
    """

    colspan: int = OPT
    rowspan: int = OPT
    colwidth: list[int] = OPT
    background: str = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeTableCell(BaseNode):
    """
    A cell within a table row.

    The tableCell node defines an individual cell within a tableRow.
    It contains block-level content such as paragraphs, lists, code blocks,
    and other block elements.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/table_cell/
    """

    type: str = TypeEnum.tableCell.value
    attrs: NodeTableCellAttrs = OPT
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
            "NodeMediaSingle",
            "NodeMediaGroup",
            "NodeDecisionList",
            "NodeTaskList",
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
        md = content_to_markdown(content=self.content, ignore_error=ignore_error)
        md = md.replace("|", "\\|")

        # Convert leading spaces to &nbsp; for HTML table rendering
        # (spaces after <br> are collapsed in HTML, so we need &nbsp;)
        lines = md.split("\n")
        processed_lines = []
        for line in lines:
            stripped = line.lstrip(" ")
            leading_spaces = len(line) - len(stripped)
            if leading_spaces > 0:
                # Replace leading spaces with &nbsp;
                line = "&nbsp;" * leading_spaces + stripped
            processed_lines.append(line)

        return "<br>".join(processed_lines)
