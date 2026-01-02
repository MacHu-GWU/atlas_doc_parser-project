# -*- coding: utf-8 -*-

import dataclasses

from ..type_enum import TypeEnum
from ..mark_or_node import BaseMark


@dataclasses.dataclass(frozen=True)
class MarkStrong(BaseMark):
    """
    Applies bold styling to text nodes.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/strong/
    """

    type: str = TypeEnum.strong.value

    def to_markdown(
        self: "MarkStrong",
        text: str,
    ) -> str:
        if text.strip():
            return f"**{text}**"
        else:
            return text
