# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: em
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_em import MarkEmMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkEm(MarkEmMixin, BaseMark):
    """
    ADF Mark: em
    """

    type: str = dataclasses.field(default=TypeEnum.em.value)
