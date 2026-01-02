# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: textColor
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_text_color import MarkTextColorMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkTextColorAttrs(Base):
    """Attributes for MarkTextColor."""
    color: str


@dataclasses.dataclass(frozen=True)
class MarkTextColor(MarkTextColorMixin, BaseMark):
    """
    ADF Mark: textColor
    """

    type: str = dataclasses.field(default=TypeEnum.textColor.value)
    attrs: MarkTextColorAttrs = OPT
