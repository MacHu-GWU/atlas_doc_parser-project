# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeEmojiAttrs(Base):
    """
    Attributes for :class:`NodeEmoji`.

    :param shortName: Required. The emoji short name identifier (e.g., ":grinning:", ":thumbsup:").
    :param id: Optional. The emoji service ID. The format varies by emoji type:
        - Standard Unicode emoji: Unicode codepoints (e.g., "1f3f3-1f308")
        - Atlassian emoji: Prefixed with "atlassian-" (e.g., "atlassian-blue_star")
        - Site/custom emoji: UUID format
    :param text: Optional. The text representation of the emoji.
        If omitted, the shortName is displayed.
    :param localId: Optional. A unique identifier for the node.
    """

    shortName: str = OPT
    id: str = OPT
    text: str = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeEmoji(BaseNode):
    """
    An inline emoji node in ADF.

    The emoji node represents emojis in three categories:

    - **Standard** — Unicode emoji (e.g., 😀, 🎉)
    - **Atlassian** — Non-standard emoji introduced by Atlassian (e.g., :atlassian:)
    - **Site** — Non-standard customer-defined emoji

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/emoji/
    """

    type: str = TypeEnum.emoji.value
    attrs: NodeEmojiAttrs = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        # Return the text representation if available, otherwise the shortName
        if isinstance(self.attrs.text, str):
            return self.attrs.text
        elif isinstance(self.attrs.shortName, str):
            return self.attrs.shortName
        else:
            raise NotImplementedError
