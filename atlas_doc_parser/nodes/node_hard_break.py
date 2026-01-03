# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeHardBreakAttrs(Base):
    """
    Attributes for :class:`NodeHardBreak`.

    :param text: Optional. The newline character (always ``"\\n"`` when present).
    :param localId: Optional. A unique identifier for the node.
    """

    text: str = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeHardBreak(BaseNode):
    """
    A hard line break element equivalent to HTML's ``<br/>`` tag.

    The hardBreak node is an inline node that inserts a line break within
    text content. It can appear inside paragraphs and other inline contexts.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/hardBreak/
    """

    type: str = TypeEnum.hardBreak.value
    attrs: T.Optional[NodeHardBreakAttrs] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return "\n\n"
