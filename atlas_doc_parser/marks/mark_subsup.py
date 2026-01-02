# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkSubsupAttrs(Base):
    """
    Attributes for :class:`MarkSubsup`.

    :param type: Required. Either "sub" for subscript or "sup" for superscript.
    """

    type: str = OPT


@dataclasses.dataclass(frozen=True)
class MarkSubsup(BaseMark):
    """
    Applies superscript or subscript styling to text nodes.

    The subsup mark is used to render text as either superscript (above the baseline)
    or subscript (below the baseline). The ``attrs.type`` attribute determines
    which style is applied.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/subsup/
    """

    type: str = TypeEnum.subsup.value
    attrs: MarkSubsupAttrs = OPT
