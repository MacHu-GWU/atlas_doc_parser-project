# -*- coding: utf-8 -*-

"""
Auto-generated ADF Mark: backgroundColor
"""

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mixins.mark_background_color import MarkBackgroundColorMixin

from .base import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkBackgroundColorAttrs(Base):
    """Attributes for MarkBackgroundColor."""

    color: str = OPT


@dataclasses.dataclass(frozen=True)
class MarkBackgroundColor(MarkBackgroundColorMixin, BaseMark):
    """
    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/backgroundColor/
    """

    type: str = TypeEnum.backgroundColor.value
    attrs: MarkBackgroundColorAttrs = OPT
