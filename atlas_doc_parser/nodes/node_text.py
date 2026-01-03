# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import BaseNode, T_MARK
from ..markdown_helpers import add_style_to_markdown


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
    marks: list[T_MARK] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ):
        md = self.text
        md = add_style_to_markdown(md=md, node=self)
        return md
