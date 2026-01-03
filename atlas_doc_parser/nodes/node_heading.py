# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode, BaseMark
from ..markdown_helpers import content_to_markdown


@dataclasses.dataclass(frozen=True)
class NodeHeadingAttrs(Base):
    """
    Attributes for :class:`NodeHeading`.

    :param level: Required. The heading level from 1 to 6, following HTML convention
        (level 1 equals ``<h1>``, level 6 equals ``<h6>``).
    :param localId: Optional. A unique identifier for the node within the document.
    """

    level: int = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeHeading(BaseNode):
    """
    A heading node in ADF.

    The heading node is a top-level block node that represents headings
    (h1 through h6) in the document. It can contain inline nodes such as
    text, mentions, emojis, and other inline elements.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/heading/
    """

    type: str = TypeEnum.heading.value
    attrs: NodeHeadingAttrs = OPT
    content: list[BaseNode] = OPT
    marks: list[BaseMark] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        md = (
            "\n\n"
            + "{} {}".format(
                "#" * self.attrs.level,
                content_to_markdown(content=self.content, ignore_error=ignore_error),
            )
            + "\n\n"
        )
        return md
