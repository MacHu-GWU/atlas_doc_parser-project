# -*- coding: utf-8 -*-

"""
NodeDoc - Root document node for Atlassian Document Format (ADF).

Reference:
    https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/doc/
"""

import typing as T
import dataclasses

from func_args.api import REQ

from ..type_enum import TypeEnum
from ..mark_or_node import BaseNode
from ..markdown_helpers import doc_content_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_block_card import NodeBlockCard
    from .node_code_block import NodeCodeBlock
    from .node_media_single import NodeMediaSingle
    from .node_paragraph import NodeParagraph
    from .node_task_list import NodeTaskList
    from .node_ordered_list import NodeOrderedList
    from .node_bullet_list import NodeBulletList
    from .node_blockquote import NodeBlockquote
    from .node_decision_list import NodeDecisionList
    from .node_embed_card import NodeEmbedCard
    from .node_extension import NodeExtension
    from .node_heading import NodeHeading
    from .node_media_group import NodeMediaGroup
    from .node_rule import NodeRule
    from .node_panel import NodePanel
    from .node_table import NodeTable
    from .node_expand import NodeExpand


@dataclasses.dataclass(frozen=True)
class NodeDoc(BaseNode):
    """
    The root node of an ADF document.

    The doc node serves as the root container representing a document in the
    Atlassian Document Format (ADF). It is the top-level node that contains
    all other block-level nodes in a Confluence page or Jira issue field.

    :param version: The ADF specification version. Currently always 1.
    :param type: The node type, always "doc".
    :param content: List of top-level block nodes (paragraphs, headings,
        lists, tables, etc.).

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/doc/
    """

    version: int = 1
    type: str = TypeEnum.doc.value
    content: list[
        T.Union[
            "NodeBlockCard",
            "NodeCodeBlock",
            "NodeMediaSingle",
            "NodeParagraph",
            "NodeTaskList",
            "NodeOrderedList",
            "NodeBulletList",
            "NodeBlockquote",
            "NodeDecisionList",
            "NodeEmbedCard",
            "NodeExtension",
            "NodeHeading",
            "NodeMediaGroup",
            "NodeRule",
            "NodePanel",
            "NodeTable",
            "NodeExpand",
        ]
    ] = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        """
        Convert the document to Markdown format.

        :param ignore_error: If True, silently skip nodes that fail to convert.
        :return: The complete document as Markdown text.
        """
        return doc_content_to_markdown(self.content, ignore_error=ignore_error)
