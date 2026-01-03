# -*- coding: utf-8 -*-

import typing as T
import textwrap
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import strip_double_empty_line, doc_content_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_paragraph import NodeParagraph
    from .node_ordered_list import NodeOrderedList
    from .node_bullet_list import NodeBulletList
    from .node_code_block import NodeCodeBlock
    from .node_media_single import NodeMediaSingle
    from .node_media_group import NodeMediaGroup
    from .node_extension import NodeExtension


@dataclasses.dataclass(frozen=True)
class NodeBlockquoteAttrs(Base):
    """
    Attributes for :class:`NodeBlockquote`.

    :param localId: Optional. A unique identifier for the node.
    """

    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeBlockquote(BaseNode):
    """
    A container for quotes.

    The blockquote node is a top-level block node that contains quoted content.
    It can include paragraphs (without marks), bullet/ordered lists, code blocks,
    media elements, and extensions.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/blockquote/
    """

    type: str = TypeEnum.blockquote.value
    attrs: NodeBlockquoteAttrs = OPT
    content: list[
        T.Union[
            "NodeParagraph",
            "NodeOrderedList",
            "NodeBulletList",
            "NodeCodeBlock",
            "NodeMediaSingle",
            "NodeMediaGroup",
            "NodeExtension",
        ]
    ] = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return (
            textwrap.indent(
                strip_double_empty_line(
                    doc_content_to_markdown(
                        content=self.content,
                        ignore_error=ignore_error,
                    )
                ),
                prefix="> ",
                predicate=lambda line: True,
            )
            + "\n"
        )