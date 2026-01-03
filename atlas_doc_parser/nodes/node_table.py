# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_table_row import NodeTableRow
    from ..marks.mark_fragment import MarkFragment


@dataclasses.dataclass(frozen=True)
class NodeTableAttrs(Base):
    """
    Attributes for :class:`NodeTable`.

    :param displayMode: Optional. Controls responsive behavior on narrow screens.
        "default" scales columns down up to 40%, "fixed" maintains original widths.
    :param isNumberColumnEnabled: Optional. If True, adds automatic row numbering.
    :param layout: Optional. Controls table alignment. Options include
        "wide", "full-width", "center", "align-end", "align-start", "default".
    :param localId: Optional. A unique identifier for the node.
    :param width: Optional. Table width in pixels. Overrides layout when specified.
        Recommended minimums: 48px for 1 column, 96px for 2 columns, 144px for 3+.
        Maximum: 1800px.
    """

    displayMode: T.Literal["default", "fixed"] = OPT
    isNumberColumnEnabled: bool = OPT
    layout: T.Literal[
        "wide",
        "full-width",
        "center",
        "align-end",
        "align-start",
        "default",
    ] = OPT
    localId: str = OPT
    width: float = OPT


@dataclasses.dataclass(frozen=True)
class NodeTable(BaseNode):
    """
    A container for defining table structures.

    The table node is a top-level block node that contains one or more tableRow
    nodes. Each tableRow contains tableCell or tableHeader nodes with paragraph
    content.

    Layout options:
        - **center**: Center-aligned (default=760px)
        - **wide**: Wider center-aligned (960px)
        - **full-width**: Stretches edge to edge (1800px)
        - **align-start/align-end**: Aligned to start/end of content area

    Note: Tables render on web and desktop only; mobile rendering is unavailable.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/table/
    """

    type: str = TypeEnum.table.value
    attrs: NodeTableAttrs = OPT
    content: list["NodeTableRow"] = REQ
    marks: list["MarkFragment"] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        lines = list()
        for row in self.content:
            try:
                md = row.to_markdown()
                lines.append(md)
                if row.content[0].is_type_of(TypeEnum.tableHeader):
                    lines.append("| " + " | ".join(["---"] * len(row.content)) + " |")
            except Exception as e:  # pragma: no cover
                if ignore_error:
                    pass
                else:
                    raise e
        return "\n".join(lines)
