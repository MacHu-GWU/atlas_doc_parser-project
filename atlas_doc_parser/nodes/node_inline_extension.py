# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeInlineExtensionAttrs(Base):
    """
    Attributes for :class:`NodeInlineExtension`.

    :param extensionKey: Required. The key that identifies the specific extension
        within an app (e.g., "pagetree").
    :param extensionType: Required. The type identifier for the extension,
        typically "com.atlassian.confluence.macro.core".
    :param parameters: Optional. Custom parameters passed to the extension.
    :param text: Optional. Fallback text content for the extension.
    :param layout: Optional. The layout mode for the extension display.
    :param localId: Optional. A unique identifier for the node.
    """

    extensionKey: str = REQ
    extensionType: str = REQ
    parameters: T.Any = OPT
    text: str = OPT
    layout: T.Literal["wide", "full-width", "default"] = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeInlineExtension(BaseNode):
    """
    An inline extension node in ADF representing an inline-level macro.

    Unlike :class:`NodeExtension` which is block-level, inline extensions appear
    within paragraph or heading content. They have no child content — just
    attributes identifying the extension. Common examples include the Page Tree
    macro rendered inline.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/inlineExtension/
    """

    type: str = TypeEnum.inlineExtension.value
    attrs: NodeInlineExtensionAttrs = REQ
    marks: list = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        ext_key = self.attrs.extensionKey
        ext_type = self.attrs.extensionType
        if isinstance(self.attrs.text, str) and self.attrs.text:
            return f"[Extension: {ext_key}] {self.attrs.text}"
        return f"[Extension: {ext_type}/{ext_key}]"
