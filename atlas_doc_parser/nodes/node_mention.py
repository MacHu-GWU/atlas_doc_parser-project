# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeMentionAttrs(Base):
    """
    Attributes for :class:`NodeMention`.

    :param id: Required. The Atlassian Account ID or collection name of the mentioned user.
    :param localId: Optional. A unique identifier for the node.
    :param text: Optional. The textual representation of the mention, including the leading @ symbol
        (e.g., "@Bradley Ayers").
    :param accessLevel: Optional. The access level of the mentioned user. Values:
        "NONE", "SITE", "APPLICATION", or "CONTAINER".
    :param userType: Optional. The type of user being mentioned. Values:
        "DEFAULT" (regular user), "SPECIAL" (special collection like "all"), or "APP" (application).
    """

    id: str = OPT
    localId: str = OPT
    text: str = OPT
    accessLevel: str = OPT
    userType: T.Literal["DEFAULT", "SPECIAL", "APP"] = OPT


@dataclasses.dataclass(frozen=True)
class NodeMention(BaseNode):
    """
    An inline mention node in ADF.

    The mention node represents a user mention (@mention) in the document.
    It can reference individual users by their Atlassian Account ID,
    or special collections like "all" for mentioning everyone.

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/mention/
    """

    type: str = TypeEnum.mention.value
    attrs: NodeMentionAttrs = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        # Return the text representation if available, otherwise format with @id
        if isinstance(self.attrs.text, str):
            return self.attrs.text
        else:
            return "@Unknown"
