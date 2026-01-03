# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_table_cell import NodeTableCell
    from .node_table_header import NodeTableHeader


@dataclasses.dataclass(frozen=True)
class NodeTableRowAttrs(Base):
    """
    Attributes for :class:`NodeTableRow`.

    :param localId: Optional. A unique identifier for the node.
    """

    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeTableRow(BaseNode):
    """
    A row within a table.

    The tableRow node defines rows within a table and serves as a container
    for table heading (tableHeader) and table cell (tableCell) nodes.

    Note: Tables are only supported on web and desktop; mobile rendering
    support for tables is not available.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/table_row/
    """

    type: str = TypeEnum.tableRow.value
    attrs: NodeTableRowAttrs = OPT
    content: list[
        T.Union[
            "NodeTableCell",
            "NodeTableHeader",
        ]
    ] = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        cells = []
        for cell in self.content:
            md = cell.to_markdown(ignore_error=ignore_error)
            cells.append(md)
        return "| " + " | ".join(cells) + " |"
