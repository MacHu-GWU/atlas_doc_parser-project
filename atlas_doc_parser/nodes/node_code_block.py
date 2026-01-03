# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import (
    content_to_markdown,
    ATLASSIAN_LANG_TO_MARKDOWN_LANG_MAPPING,
)


@dataclasses.dataclass(frozen=True)
class NodeCodeBlockAttrs(Base):
    """
    Attributes for :class:`NodeCodeBlock`.

    :param language: Optional. The programming language for syntax highlighting.
        Uses Prism language identifiers. When set to an unsupported value or
        "text", code renders as plain monospaced text.
    :param uniqueId: Optional. A unique identifier for the code block.
    :param localId: Optional. A local unique identifier for the node.
    """

    language: str = OPT
    uniqueId: str = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeCodeBlock(BaseNode):
    """
    A container for lines of code.

    The codeBlock node is a top-level block node that displays code with
    optional syntax highlighting. It contains text nodes without any marks
    (formatting).

    This node does not support any marks (maxItems: 0 in schema).

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/codeBlock/
    """

    type: str = TypeEnum.codeBlock.value
    attrs: NodeCodeBlockAttrs = OPT
    content: list[BaseNode] = OPT

    def to_markdown(
        self: "NodeCodeBlock",
        ignore_error: bool = False,
    ) -> str:
        code = content_to_markdown(
            content=self.content,
            ignore_error=ignore_error,
        )
        lang = ""
        if self.attrs is not OPT:
            if isinstance(self.attrs.language, str):
                lang = ATLASSIAN_LANG_TO_MARKDOWN_LANG_MAPPING.get(
                    self.attrs.language,
                    self.attrs.language,
                )
        if lang == "none":
            lang = ""
        return f"```{lang}\n{code}\n```"
