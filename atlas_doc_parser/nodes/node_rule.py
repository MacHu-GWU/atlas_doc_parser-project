# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeRuleAttrs(Base):
    """Attributes for :class:`NodeRule`."""

    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeRule(BaseNode):
    """
    A horizontal rule (divider) element equivalent to HTML's ``<hr/>`` tag.

    The rule node is a top-level block node that creates a visual separator
    between content sections. It requires no content and only an optional
    localId attribute.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/rule/
    """

    type: str = TypeEnum.rule.value
    attrs: NodeRuleAttrs = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return "\n\n---\n\n"
