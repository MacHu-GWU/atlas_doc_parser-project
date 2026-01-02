# -*- coding: utf-8 -*-

import dataclasses

from ..type_enum import TypeEnum
from ..mark_or_node import BaseMark


@dataclasses.dataclass(frozen=True)
class MarkUnderline(BaseMark):
    """
    Applies underline styling to text nodes.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/underline/
    """

    type: str = TypeEnum.underline.value
