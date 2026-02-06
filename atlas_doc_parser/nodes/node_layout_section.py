# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_layout_column import NodeLayoutColumn


@dataclasses.dataclass(frozen=True)
class NodeLayoutSection(BaseNode):
    """
    A layout section node containing columns for multi-column page layouts.

    The layout section is a top-level block node that contains one or more
    :class:`NodeLayoutColumn` children. In Confluence, this renders as a
    multi-column layout. Since markdown has no native column support, columns
    are rendered sequentially separated by blank lines.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/layoutSection/
    """

    type: str = TypeEnum.layoutSection.value
    content: list["NodeLayoutColumn"] = REQ
    marks: list = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        parts = []
        for column in self.content:
            col_md = column.to_markdown(ignore_error=ignore_error)
            if col_md.strip():
                parts.append(col_md)
        return "\n\n".join(parts)
