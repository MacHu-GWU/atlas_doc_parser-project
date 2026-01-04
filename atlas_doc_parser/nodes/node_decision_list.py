# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_decision_item import NodeDecisionItem


@dataclasses.dataclass(frozen=True)
class NodeDecisionListAttrs(Base):
    """
    Attributes for :class:`NodeDecisionList`.

    :param localId: A unique identifier for the decision list.
    """

    localId: str = REQ


@dataclasses.dataclass(frozen=True)
class NodeDecisionList(BaseNode):
    """
    A container for decision items.

    The decisionList node is a top-level block node that groups multiple
    decisionItem nodes together for rendering as a decision list.
    """

    type: str = TypeEnum.decisionList.value
    attrs: NodeDecisionListAttrs = REQ
    content: list["NodeDecisionItem"] = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        """
        Convert the decision list to Markdown format.

        Each decision item is rendered as a blockquote with ``>`` prefix
        on every line, separated by blank lines between items.
        """
        decision_blocks = []

        for item in self.content:
            if item.is_type_of(TypeEnum.decisionItem):
                try:
                    md = item.to_markdown(ignore_error=ignore_error)
                    decision_blocks.append(md)
                except Exception as e:
                    if ignore_error:
                        pass
                    else:
                        raise e

        # Join with blank lines between each decision
        return "\n\n".join(decision_blocks)
