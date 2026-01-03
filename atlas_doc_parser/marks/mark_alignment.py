# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkAlignmentAttrs(Base):
    """
    Attributes for :class:`MarkAlignment`.

    :param align: Required. The text alignment direction.
        Valid values are ``"center"`` or ``"end"``.
    """

    align: T.Literal["center", "end"]


@dataclasses.dataclass(frozen=True)
class MarkAlignment(BaseMark):
    """
    Sets text alignment on block-level content.

    The alignment mark controls horizontal text alignment within paragraphs
    and headings. Note that ``"start"`` (left-aligned for LTR languages) is
    the default and doesn't require a mark.

    Valid alignment values:

    - ``"center"`` - Center-aligned text
    - ``"end"`` - Right-aligned text (for LTR languages)
    """

    type: str = TypeEnum.alignment.value
    attrs: MarkAlignmentAttrs = REQ
