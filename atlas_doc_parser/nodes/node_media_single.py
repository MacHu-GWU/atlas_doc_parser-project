# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_media import NodeMedia
    from ..marks.mark_link import MarkLink


@dataclasses.dataclass(frozen=True)
class NodeMediaSingleAttrs(Base):
    """
    Attributes for :class:`NodeMediaSingle`.

    There are two variants based on the ``widthType`` attribute:

    **Percentage width** (widthType="percentage" or undefined):
        - ``layout`` is required
        - ``width`` is optional (0-100)

    **Pixel width** (widthType="pixel"):
        - ``layout``, ``width``, ``widthType`` are all required

    :param layout: Required. The layout mode for the media.
        One of: "wide", "full-width", "center", "wrap-right", "wrap-left",
        "align-end", "align-start".
    :param width: Optional for percentage, required for pixel.
        For percentage: float between 0-100.
        For pixel: the width in pixels.
    :param widthType: Optional. Either "percentage" (default) or "pixel".
    :param localId: Optional. A unique identifier for the node.
    """

    layout: T.Literal[
        "wide",
        "full-width",
        "center",
        "wrap-right",
        "wrap-left",
        "align-end",
        "align-start",
    ] = OPT
    width: float = OPT
    widthType: T.Literal["percentage", "pixel"] = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeMediaSingle(BaseNode):
    """
    A container for a single media item with layout control.

    The mediaSingle node wraps exactly one media node (image, video, or file)
    and provides layout options for how it should be displayed in the document.
    Unlike mediaGroup which handles multiple attachments, mediaSingle is used
    for displaying a single media item with full rendering support.

    Layout options:
        - **wrap-left/wrap-right**: Media floated with text wrapped around it
        - **center**: Center-aligned as a block element
        - **wide**: Center-aligned but bleeds into the margins
        - **full-width**: Stretches from edge to edge of the page
        - **align-start/align-end**: Aligned to start/end of the content area

    Note: The ``width`` attribute has no effect with ``wide`` or ``full-width`` layouts.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/mediaSingle/
    """

    type: str = TypeEnum.mediaSingle.value
    attrs: NodeMediaSingleAttrs = OPT
    content: list["NodeMedia"] = OPT
    marks: list["MarkLink"] = OPT
