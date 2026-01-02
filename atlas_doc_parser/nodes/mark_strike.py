# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: strike
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_strike import MarkStrikeMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkStrike(MarkStrikeMixin, BaseMark):
    """
    ADF Mark: strike
    """

    type: str = dataclasses.field(default=TypeEnum.strike.value)
