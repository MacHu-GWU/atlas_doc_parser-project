# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


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
    content: T.List[BaseNode] = OPT
