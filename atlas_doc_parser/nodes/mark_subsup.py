# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: subsup
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_subsup import MarkSubsupMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkSubsupAttrs(Base):
    """Attributes for MarkSubsup."""
    type: str


@dataclasses.dataclass(frozen=True)
class MarkSubsup(MarkSubsupMixin, BaseMark):
    """
    ADF Mark: subsup
    """

    type: str = dataclasses.field(default=TypeEnum.subsup.value)
    attrs: MarkSubsupAttrs = OPT
