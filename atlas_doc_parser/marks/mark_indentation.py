# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkIndentationAttrs(Base):
    """
    Attributes for :class:`MarkIndentation`.

    :param level: Required. The indentation level, an integer from 1 to 6.
    """

    level: int = OPT


@dataclasses.dataclass(frozen=True)
class MarkIndentation(BaseMark):
    """
    Applies indentation to block-level content.

    The indentation mark controls the left margin indentation of paragraphs
    and other block elements. The ``level`` attribute specifies the depth
    of indentation, ranging from 1 (minimal) to 6 (maximum).
    """

    type: str = TypeEnum.indentation.value
    attrs: MarkIndentationAttrs = OPT

    def to_markdown(
        self,
        text: str,
    ) -> str:
        return self.attrs.level * "\t"
