# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkTextColorAttrs(Base):
    """Attributes for :class:`MarkTextColor`."""

    color: str


@dataclasses.dataclass(frozen=True)
class MarkTextColor(BaseMark):
    """
    Applies color styling to text nodes.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/textColor/
    """

    type: str = TypeEnum.textColor.value
    attrs: MarkTextColorAttrs = REQ
