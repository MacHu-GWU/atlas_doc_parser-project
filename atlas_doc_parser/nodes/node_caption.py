# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_hard_break import NodeHardBreak
    from .node_mention import NodeMention
    from .node_emoji import NodeEmoji
    from .node_date import NodeDate
    from .node_placeholder import NodePlaceholder
    from .node_inline_card import NodeInlineCard
    from .node_status import NodeStatus
    from .node_text import NodeText


@dataclasses.dataclass(frozen=True)
class NodeCaptionAttrs(Base):
    """
    Attributes for :class:`NodeCaption`.

    :param localId: Optional. A unique identifier for the node.
    """

    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeCaption(BaseNode):
    """
    A caption for media elements.

    The caption node is used to add descriptive text to media elements
    such as images or videos. It contains inline content like text,
    mentions, emojis, and other inline elements.
    """

    type: str = TypeEnum.caption.value
    attrs: NodeCaptionAttrs = OPT
    content: list[
        T.Union[
            "NodeHardBreak",
            "NodeMention",
            "NodeEmoji",
            "NodeDate",
            "NodePlaceholder",
            "NodeInlineCard",
            "NodeStatus",
            "NodeText",
        ]
    ] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return ""
