# -*- coding: utf-8 -*-

"""
Mixin for ADF Mark: em
"""

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from ..nodes.mark_em import MarkEm


class MarkEmMixin:
    def to_markdown(self: "MarkEm", text: str) -> str:
        return f"*{text}*"
