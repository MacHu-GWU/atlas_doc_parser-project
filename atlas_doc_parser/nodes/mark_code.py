# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: code
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_code import MarkCodeMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkCode(MarkCodeMixin, BaseMark):
    """
    ADF Mark: code
    """

    type: str = dataclasses.field(default=TypeEnum.code.value)
