# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from ..marks.mark_link import MarkLink
    from ..marks.mark_annotation import MarkAnnotation
    from ..marks.mark_border import MarkBorder


@dataclasses.dataclass(frozen=True)
class NodeMediaInlineAttrs(Base):
    """
    Attributes for :class:`NodeMediaInline`.

    :param id: Required. The Media Services ID for API queries.
    :param collection: Required. The Media Services Collection identifier.
    :param type: Optional. The media type: "link", "file", or "image".
    :param localId: Optional. A unique identifier for the node.
    :param alt: Optional. Alternative text for the media (accessibility).
    :param occurrenceKey: Optional. Enables file deletion from collections when present.
    :param width: Optional. Display width in pixels.
    :param height: Optional. Display height in pixels.
    :param data: Optional. Additional data associated with the media.
    """

    id: str = REQ
    collection: str = REQ
    type: T.Literal["link", "file", "image"] = OPT
    localId: str = OPT
    alt: str = OPT
    occurrenceKey: str = OPT
    width: int = OPT
    height: int = OPT
    data: T.Any = OPT


@dataclasses.dataclass(frozen=True)
class NodeMediaInline(BaseNode):
    """
    An inline media node in ADF.

    The mediaInline node represents media content that appears inline within
    text content, such as images or files displayed within a paragraph.
    Unlike the media node which is a block-level element, mediaInline can
    be embedded directly in inline content.
    """

    type: str = TypeEnum.mediaInline.value
    attrs: NodeMediaInlineAttrs = REQ
    marks: list[
        T.Union[
            "MarkLink",
            "MarkAnnotation",
            "MarkBorder",
        ],
    ] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return ""
