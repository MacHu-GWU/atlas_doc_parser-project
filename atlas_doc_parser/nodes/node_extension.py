# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeExtensionAttrs(Base):
    """
    Attributes for :class:`NodeExtension`.

    :param extensionKey: Required. The key that identifies the specific extension
        within an app (e.g., "my-macro-key").
    :param extensionType: Required. The type identifier for the extension,
        typically in the format "com.atlassian.confluence.macro.core" or similar.
    :param parameters: Optional. Custom parameters passed to the extension as a
        dictionary of key-value pairs. The structure depends on the specific extension.
    :param text: Optional. Fallback text content for the extension.
    :param layout: Optional. The layout mode for the extension display.
        One of "wide", "full-width", or "default".
    :param localId: Optional. A unique identifier for the node.
    """

    extensionKey: str = REQ
    extensionType: str = REQ
    parameters: T.Any = OPT
    text: str = OPT
    layout: T.Literal["wide", "full-width", "default"] = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeExtension(BaseNode):
    """
    An extension node in ADF representing a block-level app extension.

    Extension nodes are used to embed third-party app functionality within
    Confluence pages. They represent macros and other block-level integrations
    from Atlassian Marketplace apps or custom Forge/Connect apps.

    Common use cases include:
    - Confluence macros (Table of Contents, Code Block, etc.)
    - Third-party app integrations (Jira issues, diagrams, etc.)
    - Custom Forge or Connect app extensions

    The extension is identified by its ``extensionType`` (the app identifier)
    and ``extensionKey`` (the specific extension within that app).

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/extension/
    """

    type: str = TypeEnum.extension.value
    attrs: NodeExtensionAttrs = REQ
    marks: list = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        # Extensions don't have a standard markdown representation
        # Return a placeholder with extension info
        ext_key = self.attrs.extensionKey
        ext_type = self.attrs.extensionType
        if isinstance(self.attrs.text, str) and self.attrs.text:
            return f"[Extension: {ext_key}] {self.attrs.text}"
        return f"[Extension: {ext_type}/{ext_key}]"
