# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkBackgroundColorAttrs(Base):
    """Attributes for :class:`MarkBackgroundColor`."""

    color: str


@dataclasses.dataclass(frozen=True)
class MarkBackgroundColor(BaseMark):
    """
    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/backgroundColor/
    """

    type: str = TypeEnum.backgroundColor.value
    attrs: MarkBackgroundColorAttrs = OPT
