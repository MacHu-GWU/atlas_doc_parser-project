# -*- coding: utf-8 -*-

"""
Auto-generated ADF Parser

This module provides functions to parse ADF JSON into Python objects.
"""

import typing as T

from ..type_hint import T_DATA
from ..type_enum import TypeEnum

if T.TYPE_CHECKING:  # pragma: no cover
    from ..mark_or_node import T_NODE

# =============================================================================
# Node imports
# =============================================================================
from .node_text import NodeText
from .node_rule import NodeRule
from .node_list_item import NodeListItem
from .node_bullet_list import NodeBulletList
from .node_ordered_list import NodeOrderedList
from .node_paragraph import NodeParagraph
from .node_task_item import NodeTaskItem
from .node_task_list import NodeTaskList
from .node_decision_item import NodeDecisionItem
from .node_decision_list import NodeDecisionList
from .node_emoji import NodeEmoji
from .node_hard_break import NodeHardBreak
from .node_date import NodeDate
from .node_mention import NodeMention
from .node_status import NodeStatus
from .node_heading import NodeHeading
from .node_code_block import NodeCodeBlock
from .node_inline_card import NodeInlineCard
from .node_block_card import NodeBlockCard
from .node_media import NodeMedia
from .node_media_group import NodeMediaGroup
from .node_media_single import NodeMediaSingle
from .node_embed_card import NodeEmbedCard
from .node_extension import NodeExtension
from .node_caption import NodeCaption
from .node_media_inline import NodeMediaInline
from .node_panel import NodePanel
from .node_blockquote import NodeBlockquote
from .node_expand import NodeExpand
from .node_nested_expand import NodeNestedExpand


# =============================================================================
# Node registry
# =============================================================================
NODE_TYPE_TO_CLASS_MAPPING = {
    TypeEnum.text.value: NodeText,
    TypeEnum.rule.value: NodeRule,
    TypeEnum.listItem.value: NodeListItem,
    TypeEnum.bulletList.value: NodeBulletList,
    TypeEnum.orderedList.value: NodeOrderedList,
    TypeEnum.paragraph.value: NodeParagraph,
    TypeEnum.taskItem.value: NodeTaskItem,
    TypeEnum.taskList.value: NodeTaskList,
    TypeEnum.decisionItem.value: NodeDecisionItem,
    TypeEnum.decisionList.value: NodeDecisionList,
    TypeEnum.emoji.value: NodeEmoji,
    TypeEnum.hardBreak.value: NodeHardBreak,
    TypeEnum.date.value: NodeDate,
    TypeEnum.mention.value: NodeMention,
    TypeEnum.status.value: NodeStatus,
    TypeEnum.heading.value: NodeHeading,
    TypeEnum.codeBlock.value: NodeCodeBlock,
    TypeEnum.inlineCard.value: NodeInlineCard,
    TypeEnum.blockCard.value: NodeBlockCard,
    TypeEnum.media.value: NodeMedia,
    TypeEnum.mediaGroup.value: NodeMediaGroup,
    TypeEnum.mediaSingle.value: NodeMediaSingle,
    TypeEnum.embedCard.value: NodeEmbedCard,
    TypeEnum.extension.value: NodeExtension,
    TypeEnum.caption.value: NodeCaption,
    TypeEnum.mediaInline.value: NodeMediaInline,
    TypeEnum.panel.value: NodePanel,
    TypeEnum.blockquote.value: NodeBlockquote,
    TypeEnum.expand.value: NodeExpand,
    TypeEnum.nestedExpand.value: NodeNestedExpand,
}


def parse_node(dct: T_DATA) -> "T_NODE":
    """Parse a node dictionary into a Node object."""
    type_ = dct["type"]
    klass = NODE_TYPE_TO_CLASS_MAPPING[type_]
    return klass.from_dict(dct)
