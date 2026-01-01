# -*- coding: utf-8 -*-

"""
Mixin for ADF Mark: link
"""

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from ..nodes.mark_link import MarkLink


class MarkLinkMixin:
    def to_markdown(self: "MarkLink", text: str) -> str:
        if isinstance(self.attrs.title, str):
            title = self.attrs.title
        else:
            title = text
        return f"[{title}]({self.attrs.href})"
