# -*- coding: utf-8 -*-

"""
Auto-generated ADF Parser

This module provides functions to parse ADF JSON into Python objects.
"""

import typing as T
from ..type_hint import T_DATA

if T.TYPE_CHECKING:  # pragma: no cover
    from .base import T_MARK, T_NODE

# =============================================================================
# Mark imports
# =============================================================================
from .mark_alignment import MarkAlignment
from .mark_annotation import MarkAnnotation
from .mark_background_color import MarkBackgroundColor
from .mark_border import MarkBorder
from .mark_breakout import MarkBreakout
from .mark_code import MarkCode
from .mark_data_consumer import MarkDataConsumer
from .mark_em import MarkEm
from .mark_fragment import MarkFragment
from .mark_indentation import MarkIndentation
from .mark_link import MarkLink
from .mark_strike import MarkStrike
from .mark_strong import MarkStrong
from .mark_subsup import MarkSubsup
from .mark_text_color import MarkTextColor
from .mark_underline import MarkUnderline

# =============================================================================
# Node imports
# =============================================================================
from .node_block_card import NodeBlockCard
from .node_block_task_item import NodeBlockTaskItem
from .node_blockquote import NodeBlockquote
from .node_bodied_extension import NodeBodiedExtension
from .node_bodied_sync_block import NodeBodiedSyncBlock
from .node_bullet_list import NodeBulletList
from .node_caption import NodeCaption
from .node_code_block import NodeCodeBlock
from .node_date import NodeDate
from .node_decision_item import NodeDecisionItem
from .node_decision_list import NodeDecisionList
from .node_doc import NodeDoc
from .node_embed_card import NodeEmbedCard
from .node_emoji import NodeEmoji
from .node_expand import NodeExpand
from .node_extension import NodeExtension
from .node_hard_break import NodeHardBreak
from .node_heading import NodeHeading
from .node_inline_card import NodeInlineCard
from .node_inline_extension import NodeInlineExtension
from .node_layout_column import NodeLayoutColumn
from .node_layout_section import NodeLayoutSection
from .node_list_item import NodeListItem
from .node_media import NodeMedia
from .node_media_group import NodeMediaGroup
from .node_media_inline import NodeMediaInline
from .node_media_single import NodeMediaSingle
from .node_mention import NodeMention
from .node_nested_expand import NodeNestedExpand
from .node_ordered_list import NodeOrderedList
from .node_panel import NodePanel
from .node_paragraph import NodeParagraph
from .node_placeholder import NodePlaceholder
from .node_rule import NodeRule
from .node_status import NodeStatus
from .node_sync_block import NodeSyncBlock
from .node_table import NodeTable
from .node_table_cell import NodeTableCell
from .node_table_header import NodeTableHeader
from .node_table_row import NodeTableRow
from .node_task_item import NodeTaskItem
from .node_task_list import NodeTaskList
from .node_text import NodeText


# =============================================================================
# Mark registry
# =============================================================================
_mark_type_to_class_mapping = {
    "alignment": MarkAlignment,
    "annotation": MarkAnnotation,
    "backgroundColor": MarkBackgroundColor,
    "border": MarkBorder,
    "breakout": MarkBreakout,
    "code": MarkCode,
    "dataConsumer": MarkDataConsumer,
    "em": MarkEm,
    "fragment": MarkFragment,
    "indentation": MarkIndentation,
    "link": MarkLink,
    "strike": MarkStrike,
    "strong": MarkStrong,
    "subsup": MarkSubsup,
    "textColor": MarkTextColor,
    "underline": MarkUnderline,
}


def parse_mark(dct: T_DATA) -> "T_MARK":
    """Parse a mark dictionary into a Mark object."""
    type_ = dct["type"]
    klass = _mark_type_to_class_mapping[type_]
    return klass.from_dict(dct)


# =============================================================================
# Node registry
# =============================================================================
_node_type_to_class_mapping = {
    "blockCard": NodeBlockCard,
    "blockTaskItem": NodeBlockTaskItem,
    "blockquote": NodeBlockquote,
    "bodiedExtension": NodeBodiedExtension,
    "bodiedSyncBlock": NodeBodiedSyncBlock,
    "bulletList": NodeBulletList,
    "caption": NodeCaption,
    "codeBlock": NodeCodeBlock,
    "date": NodeDate,
    "decisionItem": NodeDecisionItem,
    "decisionList": NodeDecisionList,
    "doc": NodeDoc,
    "embedCard": NodeEmbedCard,
    "emoji": NodeEmoji,
    "expand": NodeExpand,
    "extension": NodeExtension,
    "hardBreak": NodeHardBreak,
    "heading": NodeHeading,
    "inlineCard": NodeInlineCard,
    "inlineExtension": NodeInlineExtension,
    "layoutColumn": NodeLayoutColumn,
    "layoutSection": NodeLayoutSection,
    "listItem": NodeListItem,
    "media": NodeMedia,
    "mediaGroup": NodeMediaGroup,
    "mediaInline": NodeMediaInline,
    "mediaSingle": NodeMediaSingle,
    "mention": NodeMention,
    "nestedExpand": NodeNestedExpand,
    "orderedList": NodeOrderedList,
    "panel": NodePanel,
    "paragraph": NodeParagraph,
    "placeholder": NodePlaceholder,
    "rule": NodeRule,
    "status": NodeStatus,
    "syncBlock": NodeSyncBlock,
    "table": NodeTable,
    "tableCell": NodeTableCell,
    "tableHeader": NodeTableHeader,
    "tableRow": NodeTableRow,
    "taskItem": NodeTaskItem,
    "taskList": NodeTaskList,
    "text": NodeText,
}


def parse_node(dct: T_DATA) -> "T_NODE":
    """Parse a node dictionary into a Node object."""
    type_ = dct["type"]
    klass = _node_type_to_class_mapping[type_]
    return klass.from_dict(dct)
