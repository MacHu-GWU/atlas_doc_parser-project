# -*- coding: utf-8 -*-

import dataclasses

from ..type_enum import TypeEnum
from ..mark_or_node import BaseMark


@dataclasses.dataclass(frozen=True)
class MarkCode(BaseMark):
    """
    Inline code mark for text nodes.

    This mark applies inline code styling to text. It can only be combined
    with the ``link`` mark.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/code/
    """

    type: str = TypeEnum.code.value

    def to_markdown(
        self,
        text: str,
    ) -> str:
        if "\n" in text:
            raise ValueError(
                "Code mark cannot contain newlines in markdown representation."
            )
        if text.strip():
            return f"`` {text} ``"
        else:
            return text
