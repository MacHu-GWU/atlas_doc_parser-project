# -*- coding: utf-8 -*-

"""
Mixin for ADF Mark: code
"""

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from ..nodes.mark_code import MarkCode


class MarkCodeMixin:
    def to_markdown(self: "MarkCode", text: str) -> str:
        return f"`{text}`"
