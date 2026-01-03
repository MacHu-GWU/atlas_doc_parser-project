# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode, BaseMark
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
    from ..marks.mark_alignment import MarkAlignment
    from ..marks.mark_indentation import MarkIndentation


@dataclasses.dataclass(frozen=True)
class NodeHeadingAttrs(Base):
    """
    Attributes for :class:`NodeHeading`.

    :param level: Required. The heading level from 1 to 6, following HTML convention
        (level 1 equals ``<h1>``, level 6 equals ``<h6>``).
    :param localId: Optional. A unique identifier for the node within the document.
    """

    level: int = REQ
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeHeading(BaseNode):
    """
    A heading node in ADF.

    The heading node is a top-level block node that represents headings
    (h1 through h6) in the document. It can contain inline nodes such as
    text, mentions, emojis, and other inline elements.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/heading/
    """

    type: str = TypeEnum.heading.value
    attrs: NodeHeadingAttrs = REQ
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
    marks: list[
        T.Union[
            "MarkAlignment",
            "MarkIndentation",
        ]
    ] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        md = (
            "\n\n"
            + "{} {}".format(
                "#" * self.attrs.level,
                content_to_markdown(content=self.content, ignore_error=ignore_error),
            )
            + "\n\n"
        )
        return md
