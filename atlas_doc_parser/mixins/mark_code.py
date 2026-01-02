# -*- coding: utf-8 -*-

"""
Mixin for ADF Mark: code
"""

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from ..nodes.mark_code import MarkCode


class MarkCodeMixin:
    def to_markdown(self: "MarkCode", text: str) -> str:
        if "\n" in text:
            raise ValueError("Code mark cannot contain newlines in markdown representation.")
        if text.strip():
            return f"`` {text} ``"
        else:
            return text
