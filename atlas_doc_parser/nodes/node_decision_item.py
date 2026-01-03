# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import content_to_markdown


@dataclasses.dataclass(frozen=True)
class NodeDecisionItemAttrs(Base):
    """
    Attributes for :class:`NodeDecisionItem`.

    :param localId: A unique identifier for the decision item.
    :param state: The state of the decision (e.g., "DECIDED").
    """

    localId: str = OPT
    state: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeDecisionItem(BaseNode):
    """
    A single decision item within a decisionList.

    The decisionItem node represents a decision entry in a decision list.
    It contains inline content and has attributes for tracking its state.
    """

    type: str = TypeEnum.decisionItem.value
    attrs: NodeDecisionItemAttrs = OPT
    content: list[BaseNode] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return content_to_markdown(content=self.content, ignore_error=ignore_error)
