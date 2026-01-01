# -*- coding: utf-8 -*-

"""
Mixin for ADF Mark: strike
"""

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from ..nodes.mark_strike import MarkStrike


class MarkStrikeMixin:
    def to_markdown(self: "MarkStrike", text: str) -> str:
        return f"~~{text}~~"
