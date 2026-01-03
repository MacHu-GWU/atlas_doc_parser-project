# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkLinkAttrs(Base):
    """
    Attributes for :class:`MarkLink`.

    :param href: Required. The hyperlink destination URI.
    :param title: Optional. The hyperlink title (HTML title attribute).
    :param id: Optional. String identifier.
    :param collection: Optional. String value for collection.
    :param occurrenceKey: Optional. String value for occurrence key.
    """

    href: str = REQ
    title: str = OPT
    id: str = OPT
    collection: str = OPT
    occurrenceKey: str = OPT


@dataclasses.dataclass(frozen=True)
class MarkLink(BaseMark):
    """
    Sets a hyperlink on text nodes.

    The link mark applies exclusively to ``text`` nodes and creates a clickable
    hyperlink. The ``href`` attribute is required and specifies the destination URL.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/link/
    """

    type: str = TypeEnum.link.value
    attrs: MarkLinkAttrs = REQ

    def to_markdown(
        self,
        text: str,
    ) -> str:
        if isinstance(self.attrs.title, str):
            title = self.attrs.title
        else:
            title = text
        return f"[{title}]({self.attrs.href})"
