# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

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

    localId: str = REQ
    state: str = REQ


@dataclasses.dataclass(frozen=True)
class NodeDecisionItem(BaseNode):
    """
    A single decision item within a decisionList.

    The decisionItem node represents a decision entry in a decision list.
    It contains inline content and has attributes for tracking its state.
    """

    type: str = TypeEnum.decisionItem.value
    attrs: NodeDecisionItemAttrs = REQ
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
        """
        Convert the decision item to Markdown format.

        Each line is prefixed with ``> `` for blockquote formatting.
        Leading empty lines after the first content line are skipped,
        and consecutive empty lines are collapsed.
        """
        # Get raw content markdown
        item_content = content_to_markdown(
            content=self.content,
            ignore_error=ignore_error,
        ).rstrip()

        # Split into lines and prefix each with "> "
        raw_lines = item_content.split("\n")

        # Process lines:
        # 1. Skip empty lines that appear immediately after the first line
        #    (the decision title line)
        # 2. Collapse consecutive empty lines
        # 3. Keep single empty lines between content
        prefixed_lines = []
        line_count = 0  # Count of non-empty content lines
        prev_was_empty = False
        for line in raw_lines:
            line = line.rstrip()
            is_empty = not line

            if is_empty:
                # Skip empty lines after only the first content line
                # (skip leading blanks after title)
                # Also skip consecutive empty lines
                if line_count <= 1 or prev_was_empty:
                    continue
                prefixed_lines.append(">")
                prev_was_empty = True
            else:
                prefixed_lines.append(f"> {line}")
                line_count += 1
                prev_was_empty = False

        return "\n".join(prefixed_lines)
