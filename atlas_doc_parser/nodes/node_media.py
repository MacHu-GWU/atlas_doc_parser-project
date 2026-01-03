# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode, T_MARK

if T.TYPE_CHECKING:  # pragma: no cover
    from ..marks.mark_link import MarkLink
    from ..marks.mark_annotation import MarkAnnotation
    from ..marks.mark_border import MarkBorder


@dataclasses.dataclass(frozen=True)
class NodeMediaAttrs(Base):
    """
    Attributes for :class:`NodeMedia`.

    There are two variants based on the ``type`` attribute:

    **Internal media** (type="file" or "link"):
        - ``type``, ``id``, ``collection`` are required

    **External media** (type="external"):
        - ``type``, ``url`` are required

    :param type: Required. The media type: "file", "link", or "external".
    :param id: Required for internal media. The Media Services ID for API queries.
    :param collection: Required for internal media. The Media Services Collection identifier.
    :param url: Required for external media. The external URL of the media.
    :param localId: Optional. A unique identifier for the node.
    :param alt: Optional. Alternative text for the media (accessibility).
    :param width: Optional. Display width in pixels.
    :param height: Optional. Display height in pixels.
    :param occurrenceKey: Optional. Enables file deletion from collections when present.
    """

    type: T.Literal["file", "link", "external"] = OPT
    id: str = OPT
    collection: str = OPT
    url: str = OPT
    localId: str = OPT
    alt: str = OPT
    width: int = OPT
    height: int = OPT
    occurrenceKey: str = OPT

    def is_file_type(self) -> bool:
        return self.type == "file"

    def is_link_type(self) -> bool:
        return self.type == "link"

    def is_external_type(self) -> bool:
        return self.type == "external"


@dataclasses.dataclass(frozen=True)
class NodeMedia(BaseNode):
    """
    A media node in ADF representing a file, link, or external media.

    The media node represents a single file or link stored in media services.
    It is a child block node that can only be nested within ``mediaGroup``
    or ``mediaSingle`` nodes.

    There are two variants:

    - **Internal media** (type="file" or "link"): References media stored in
      Atlassian's Media Services, identified by ``id`` and ``collection``.
    - **External media** (type="external"): References external media via ``url``.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/media/
    """

    type: str = TypeEnum.media.value
    attrs: NodeMediaAttrs = REQ
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
        # For external media, return as markdown image/link
        if self.attrs.type == "external" and isinstance(self.attrs.url, str):
            alt = self.attrs.alt if isinstance(self.attrs.alt, str) else "media"
            return f"![{alt}]({self.attrs.url})"
        # For internal media, return placeholder with id
        elif isinstance(self.attrs.id, str):
            alt = self.attrs.alt if isinstance(self.attrs.alt, str) else "media"
            return f"![{alt}](media:{self.attrs.id})"
        else:
            return "[media]"
