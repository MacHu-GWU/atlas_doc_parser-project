# -*- coding: utf-8 -*-

import dataclasses

from ..type_enum import TypeEnum
from ..mark_or_node import BaseMark


@dataclasses.dataclass(frozen=True)
class MarkEm(BaseMark):
    """
    Applies italic styling to text nodes.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/em/
    """

    type: str = TypeEnum.em.value

    def to_markdown(
        self,
        text: str,
    ) -> str:
        if text.strip():
            return f"*{text}*"
        else:
            return text
