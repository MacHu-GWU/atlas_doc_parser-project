# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import doc_content_to_markdown, add_style_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_paragraph import NodeParagraph
    from .node_panel import NodePanel
    from .node_blockquote import NodeBlockquote
    from .node_ordered_list import NodeOrderedList
    from .node_bullet_list import NodeBulletList
    from .node_rule import NodeRule
    from .node_heading import NodeHeading
    from .node_code_block import NodeCodeBlock
    from .node_media_group import NodeMediaGroup
    from .node_media_single import NodeMediaSingle
    from .node_decision_list import NodeDecisionList
    from .node_task_list import NodeTaskList
    from .node_table import NodeTable
    from .node_block_card import NodeBlockCard
    from .node_embed_card import NodeEmbedCard
    from .node_extension import NodeExtension
    from .node_nested_expand import NodeNestedExpand


@dataclasses.dataclass(frozen=True)
class NodeBodiedExtensionAttrs(Base):
    """
    Attributes for :class:`NodeBodiedExtension`.

    :param extensionKey: Required. The key that identifies the specific extension
        within an app (e.g., "details", "excerpt", "info").
    :param extensionType: Required. The type identifier for the extension,
        typically "com.atlassian.confluence.macro.core".
    :param parameters: Optional. Custom parameters passed to the extension.
    :param text: Optional. Fallback text content for the extension.
    :param layout: Optional. The layout mode for the extension display.
    :param localId: Optional. A unique identifier for the node.
    """

    extensionKey: str = REQ
    extensionType: str = REQ
    parameters: T.Any = OPT
    text: str = OPT
    layout: T.Literal["wide", "full-width", "default"] = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeBodiedExtension(BaseNode):
    """
    A bodied extension node in ADF representing a block-level macro with content.

    Unlike :class:`NodeExtension` which is a leaf node, bodied extensions contain
    block-level child content. Common Confluence macros that use this type include
    Excerpt, Info, Note, Warning, Page Properties (details), and other macros
    that wrap content.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/bodiedExtension/
    """

    type: str = TypeEnum.bodiedExtension.value
    attrs: NodeBodiedExtensionAttrs = REQ
    content: list[
        T.Union[
            "NodeParagraph",
            "NodePanel",
            "NodeBlockquote",
            "NodeOrderedList",
            "NodeBulletList",
            "NodeRule",
            "NodeHeading",
            "NodeCodeBlock",
            "NodeMediaGroup",
            "NodeMediaSingle",
            "NodeDecisionList",
            "NodeTaskList",
            "NodeTable",
            "NodeBlockCard",
            "NodeEmbedCard",
            "NodeExtension",
            "NodeNestedExpand",
        ]
    ] = REQ
    marks: list = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        md = doc_content_to_markdown(content=self.content, ignore_error=ignore_error)
        md = add_style_to_markdown(md, self)
        return md
