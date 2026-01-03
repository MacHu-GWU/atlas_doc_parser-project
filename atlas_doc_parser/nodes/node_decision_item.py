# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import content_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_text import NodeText
    from .node_date import NodeDate
    from .node_emoji import NodeEmoji
    from .node_hard_break import NodeHardBreak
    from .node_inline_card import NodeInlineCard
    from .node_mention import NodeMention
    from .node_status import NodeStatus
    from .node_placeholder import NodePlaceholder
    from .node_inline_extension import NodeInlineExtension
    from .node_media_inline import NodeMediaInline


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
    content: list[
        T.Union[
            "NodeText",
            "NodeDate",
            "NodeEmoji",
            "NodeHardBreak",
            "NodeInlineCard",
            "NodeMention",
            "NodeStatus",
            "NodePlaceholder",
            "NodeInlineExtension",
            "NodeMediaInline",
        ]
    ] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return content_to_markdown(content=self.content, ignore_error=ignore_error)
