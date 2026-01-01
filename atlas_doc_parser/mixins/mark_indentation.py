# -*- coding: utf-8 -*-

"""
Mixin for ADF Mark: indentation
"""

import typing as T
import textwrap

from ..constants import TAB

if T.TYPE_CHECKING:  # pragma: no cover
    from ..nodes.mark_indentation import MarkIndentation


class MarkIndentationMixin:
    def to_markdown(self: "MarkIndentation", text: str) -> str:
        return textwrap.indent(
            text=text,
            prefix=TAB * self.attrs.level,
        )
