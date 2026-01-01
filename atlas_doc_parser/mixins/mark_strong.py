# -*- coding: utf-8 -*-

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from ..nodes.mark_strong import MarkStrong


class MarkStrongMixin:
    def to_markdown(self: "MarkStrong", text: str) -> str:
        if text.strip():
            return f"**{text}**"
        else:
            return text
