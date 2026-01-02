# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: backgroundColor
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_background_color import MarkBackgroundColorMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkBackgroundColorAttrs(Base):
    """Attributes for MarkBackgroundColor."""
    color: str


@dataclasses.dataclass(frozen=True)
class MarkBackgroundColor(MarkBackgroundColorMixin, BaseMark):
    """
    ADF Mark: backgroundColor
    """

    type: str = dataclasses.field(default=TypeEnum.backgroundColor.value)
    attrs: MarkBackgroundColorAttrs = OPT
