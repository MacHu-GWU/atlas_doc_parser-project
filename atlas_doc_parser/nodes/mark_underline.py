# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: underline
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_underline import MarkUnderlineMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkUnderline(MarkUnderlineMixin, BaseMark):
    """
    ADF Mark: underline
    """

    type: str = dataclasses.field(default=TypeEnum.underline.value)
