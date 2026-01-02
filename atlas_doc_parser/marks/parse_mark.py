# -*- coding: utf-8 -*-

"""
Auto-generated ADF Parser

This module provides functions to parse ADF JSON into Python objects.
"""

import typing as T

from ..type_hint import T_DATA
from ..type_enum import TypeEnum

if T.TYPE_CHECKING:  # pragma: no cover
    from ..mark_or_node import T_MARK

# =============================================================================
# Mark imports
# =============================================================================
from .mark_background_color import MarkBackgroundColor
from .mark_code import MarkCode
from .mark_em import MarkEm
from .mark_link import MarkLink
from .mark_strike import MarkStrike
from .mark_strong import MarkStrong
from .mark_subsup import MarkSubsup
from .mark_text_color import MarkTextColor
from .mark_underline import MarkUnderline


# =============================================================================
# Mark registry
# =============================================================================
_mark_type_to_class_mapping = {
    TypeEnum.backgroundColor.value: MarkBackgroundColor,
    TypeEnum.code.value: MarkCode,
    TypeEnum.em.value: MarkEm,
    TypeEnum.link.value: MarkLink,
    TypeEnum.strike.value: MarkStrike,
    TypeEnum.strong.value: MarkStrong,
    TypeEnum.subsup.value: MarkSubsup,
    TypeEnum.textColor.value: MarkTextColor,
    TypeEnum.underline.value: MarkUnderline,
}


def parse_mark(dct: T_DATA) -> "T_MARK":
    """Parse a mark dictionary into a Mark object."""
    type_ = dct["type"]
    klass = _mark_type_to_class_mapping[type_]
    return klass.from_dict(dct)
