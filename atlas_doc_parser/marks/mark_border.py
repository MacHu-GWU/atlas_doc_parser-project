# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkBorderAttrs(Base):
    """
    Attributes for :class:`MarkBorder`.

    :param size: Required. Border size (1-3).
    :param color: Required. Border color as hex string (#RRGGBB or #RRGGBBAA).
    """

    size: int = REQ
    color: str = REQ


@dataclasses.dataclass(frozen=True)
class MarkBorder(BaseMark):
    """
    Applies a border style to content.

    The border mark adds a visible border around the marked content with
    configurable size and color.
    """

    type: str = TypeEnum.border.value
    attrs: MarkBorderAttrs = REQ
