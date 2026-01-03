# -*- coding: utf-8 -*-

import dataclasses
from datetime import datetime, timezone

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeDateAttrs(Base):
    """
    Attributes for :class:`NodeDate`.

    :param timestamp: Required. A UNIX timestamp in milliseconds stored as a string.
    :param localId: Optional. A unique identifier for the node.
    """

    timestamp: str = REQ
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeDate(BaseNode):
    """
    Displays a date in the user's locale.

    The date node is an inline node that shows a date value. The timestamp
    is stored as a UNIX timestamp in milliseconds (as a string), and the
    rendering automatically adjusts to display dates according to each
    user's locale preferences.

    This node does not support any marks (formatting options).

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/date/
    """

    type: str = TypeEnum.date.value
    attrs: NodeDateAttrs = REQ

    def to_markdown(
        self: "NodeDate",
        ignore_error: bool = False,
    ) -> str:
        sec = int(self.attrs.timestamp) / 1000
        return str(datetime.fromtimestamp(sec, tz=timezone.utc).date())
