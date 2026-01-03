# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import typing

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkBreakoutAttrs(Base):
    """Attributes for :class:`MarkBreakout`."""

    mode: typing.Literal['wide', 'full-width']
    """Breakout mode. One of 'wide' or 'full-width'."""
    width: int = OPT
    """Optional width value."""


@dataclasses.dataclass(frozen=True)
class MarkBreakout(BaseMark):
    """
    Breakout mark for layout width control.

    This mark controls the layout breakout mode of elements, allowing them
    to extend beyond the normal content width.
    """

    type: str = TypeEnum.breakout.value
    attrs: MarkBreakoutAttrs = OPT
