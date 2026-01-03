# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import content_to_markdown


@dataclasses.dataclass(frozen=True)
class NodeListItemAttrs(Base):
    """
    Attributes for :class:`NodeListItem`.

    :param localId: Optional. A unique identifier for the node.
    """

    localId: T.Optional[str] = OPT


@dataclasses.dataclass(frozen=True)
class NodeListItem(BaseNode):
    """
    A single item within an ordered or unordered list.

    The listItem node is a child of bulletList or orderedList nodes.
    It contains block-level content such as paragraphs, nested lists,
    code blocks, or media elements.
    """

    type: str = TypeEnum.listItem.value
    attrs: T.Optional[NodeListItemAttrs] = OPT
    content: T.List[BaseNode] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return content_to_markdown(content=self.content, ignore_error=ignore_error)
