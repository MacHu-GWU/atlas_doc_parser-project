# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import content_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_paragraph import NodeParagraph
    from .node_code_block import NodeCodeBlock
    from .node_bullet_list import NodeBulletList
    from .node_ordered_list import NodeOrderedList
    from .node_task_list import NodeTaskList
    from .node_media_single import NodeMediaSingle
    from .node_extension import NodeExtension


@dataclasses.dataclass(frozen=True)
class NodeListItemAttrs(Base):
    """
    Attributes for :class:`NodeListItem`.

    :param localId: Optional. A unique identifier for the node.
    """

    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeListItem(BaseNode):
    """
    A single item within an ordered or unordered list.

    The listItem node is a child of bulletList or orderedList nodes.
    It contains block-level content such as paragraphs, nested lists,
    code blocks, or media elements.
    """

    type: str = TypeEnum.listItem.value
    attrs: NodeListItemAttrs = OPT
    content: list[
        T.Union[
            "NodeParagraph",
            "NodeCodeBlock",
            "NodeBulletList",
            "NodeOrderedList",
            "NodeTaskList",
            "NodeMediaSingle",
            "NodeExtension",
        ]
    ] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return content_to_markdown(content=self.content, ignore_error=ignore_error)
