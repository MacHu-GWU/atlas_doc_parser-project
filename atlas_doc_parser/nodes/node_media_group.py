# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_media import NodeMedia


@dataclasses.dataclass(frozen=True)
class NodeMediaGroup(BaseNode):
    """
    A container node for grouping multiple media items.

    The mediaGroup node serves as a container for multiple media items,
    distinguishing it from mediaSingle which displays a single media item.
    It is a top-level block node that must contain one or more media nodes.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/mediaGroup/
    """

    type: str = TypeEnum.mediaGroup.value
    content: list["NodeMedia"] = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return ""
