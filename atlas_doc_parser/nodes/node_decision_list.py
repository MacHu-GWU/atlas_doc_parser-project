# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeDecisionListAttrs(Base):
    """
    Attributes for :class:`NodeDecisionList`.

    :param localId: A unique identifier for the decision list.
    """

    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeDecisionList(BaseNode):
    """
    A container for decision items.

    The decisionList node is a top-level block node that groups multiple
    decisionItem nodes together for rendering as a decision list.
    """

    type: str = TypeEnum.decisionList.value
    attrs: NodeDecisionListAttrs = OPT
    content: T.List[BaseNode] = OPT
