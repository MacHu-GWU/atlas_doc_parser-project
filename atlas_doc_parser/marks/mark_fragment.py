# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkFragmentAttrs(Base):
    """
    Attributes for :class:`MarkFragment`.

    :param localId: Required. A unique local identifier for the fragment (min length: 1).
    :param name: Optional. A human-readable name for the fragment.
    """

    localId: str
    name: str = OPT


@dataclasses.dataclass(frozen=True)
class MarkFragment(BaseMark):
    """
    Marks a text range as a named fragment for linking or referencing.

    The fragment mark identifies a portion of content with a unique local ID,
    allowing it to be referenced or linked to from elsewhere in the document
    or from external sources.
    """

    type: str = TypeEnum.fragment.value
    attrs: MarkFragmentAttrs = REQ
