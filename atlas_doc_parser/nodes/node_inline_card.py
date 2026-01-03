# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeInlineCardAttrs(Base):
    """
    Attributes for :class:`NodeInlineCard`.

    Either ``url`` or ``data`` must be provided, but not both.

    :param url: The URI/web address for the linked resource. Mutually exclusive with ``data``.
    :param data: A JSON-LD representation of the link content. Mutually exclusive with ``url``.
    :param localId: Optional. A unique identifier for the node.
    """

    url: str = OPT
    data: T.Any = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeInlineCard(BaseNode):
    """
    An inline card (smart link) node in ADF.

    The inlineCard node represents an Atlassian link card with a type icon
    and content description derived from the link. It displays as an inline
    element within text content.

    The card can be defined either by a URL (which Atlassian resolves to display
    rich content) or by providing JSON-LD data directly.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/inlineCard/
    """

    type: str = TypeEnum.inlineCard.value
    attrs: NodeInlineCardAttrs = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        if isinstance(self.attrs.url, str):
            return f"[{self.attrs.url}]({self.attrs.url})"
        else:
            raise NotImplementedError
