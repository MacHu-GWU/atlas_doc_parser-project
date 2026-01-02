# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: link
"""

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_link import MarkLinkMixin
from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkLinkAttrs(Base):
    """Attributes for MarkLink."""
    href: str
    collection: str = OPT
    id: str = OPT
    occurrenceKey: str = OPT
    title: str = OPT


@dataclasses.dataclass(frozen=True)
class MarkLink(MarkLinkMixin, BaseMark):
    """
    ADF Mark: link
    """

    type: str = dataclasses.field(default=TypeEnum.link.value)
    attrs: MarkLinkAttrs = OPT
