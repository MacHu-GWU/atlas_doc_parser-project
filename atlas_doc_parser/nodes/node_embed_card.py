# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeEmbedCardAttrs(Base):
    """
    Attributes for :class:`NodeEmbedCard`.

    :param url: Required. The URL for the embedded content.
    :param layout: Required. Layout mode for the embedded card. One of:
        wide, full-width, center, wrap-right, wrap-left, align-end, align-start.
    :param width: Optional. Width as a percentage (0-100).
    :param originalHeight: Optional. Original height of the embedded content.
    :param originalWidth: Optional. Original width of the embedded content.
    :param localId: Optional. A unique identifier for the node.
    """

    url: str = REQ
    layout: T.Literal[
        "wide",
        "full-width",
        "center",
        "wrap-right",
        "wrap-left",
        "align-end",
        "align-start",
    ] = REQ
    width: float = OPT
    originalHeight: float = OPT
    originalWidth: float = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeEmbedCard(BaseNode):
    """
    An embedded content card node in ADF.

    The embedCard node displays embedded content from external sources
    (such as videos, documents, or other rich media) as a block element.
    Unlike inlineCard and blockCard which show link previews, embedCard
    renders the actual embedded content within the document.

    This is a top-level block node that supports various layout options
    for positioning the embedded content.
    """

    type: str = TypeEnum.embedCard.value
    attrs: NodeEmbedCardAttrs = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return f"\n[{self.attrs.url}]({self.attrs.url})\n"
