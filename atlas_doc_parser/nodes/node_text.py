# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import BaseNode
from ..markdown_helpers import add_style_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from ..marks.mark_link import MarkLink
    from ..marks.mark_em import MarkEm
    from ..marks.mark_strong import MarkStrong
    from ..marks.mark_strike import MarkStrike
    from ..marks.mark_subsup import MarkSubsup
    from ..marks.mark_underline import MarkUnderline
    from ..marks.mark_text_color import MarkTextColor
    from ..marks.mark_annotation import MarkAnnotation
    from ..marks.mark_background_color import MarkBackgroundColor


@dataclasses.dataclass(frozen=True)
class NodeText(BaseNode):
    """
    Holds document text within the ADF structure.

    The text node is an inline node that contains the actual text content.
    It can have formatting marks applied such as strong, em, link, code,
    strike, subsup, textColor, and underline.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/text/
    """

    type: str = TypeEnum.text.value
    text: str = OPT
    marks: list[
        T.Union[
            "MarkLink",
            "MarkEm",
            "MarkStrong",
            "MarkStrike",
            "MarkSubsup",
            "MarkUnderline",
            "MarkTextColor",
            "MarkAnnotation",
            "MarkBackgroundColor",
        ]
    ] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ):
        md = self.text
        md = add_style_to_markdown(md=md, node=self)
        return md
