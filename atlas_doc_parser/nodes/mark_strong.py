# -*- coding: utf-8 -*-

import dataclasses

from ..type_enum import TypeEnum
from ..mixins.mark_strong import MarkStrongMixin

from .base import BaseMark


@dataclasses.dataclass(frozen=True)
class MarkStrong(BaseMark, MarkStrongMixin):
    type: str = dataclasses.field(default=TypeEnum.strong.value)

    def to_markdown(self, text: str) -> str:
        return f"**{text}**"
