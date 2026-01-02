# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: strong
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_strong import MarkStrongMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkStrong(MarkStrongMixin, BaseMark):
    """
    ADF Mark: strong
    """

    type: str = dataclasses.field(default=TypeEnum.strong.value)
