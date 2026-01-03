# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeStatusAttrs(Base):
    """
    Attributes for :class:`NodeStatus`.

    :param text: Required. The textual representation of the status.
    :param color: Required. Visual indicator color. One of: neutral, purple,
        blue, red, yellow, green.
    :param localId: Optional. A unique identifier for the node.
    :param style: Optional. Style information for the status.
    """

    text: str = REQ
    color: T.Literal["neutral", "purple", "blue", "red", "yellow", "green"] = REQ
    localId: str = OPT
    style: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeStatus(BaseNode):
    """
    Represents the state of work within documents.

    The status node is an inline node that displays a status lozenge with
    text and a background color. It is commonly used to indicate workflow
    states like "In Progress", "Done", "To Do", etc.

    This node does not support any marks (formatting options).

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/status/
    """

    type: str = TypeEnum.status.value
    attrs: NodeStatusAttrs = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return f"`{self.attrs.text}`"
