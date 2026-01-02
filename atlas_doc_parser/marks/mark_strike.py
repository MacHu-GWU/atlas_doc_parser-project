# -*- coding: utf-8 -*-

import dataclasses

from ..type_enum import TypeEnum
from ..mark_or_node import BaseMark


@dataclasses.dataclass(frozen=True)
class MarkStrike(BaseMark):
    """
    Applies strike-through styling to text nodes.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/strike/
    """

    type: str = TypeEnum.strike.value

    def to_markdown(
        self: "MarkStrike",
        text: str,
    ) -> str:
        if text.strip():
            return f"~~{text}~~"
        else:
            return text
