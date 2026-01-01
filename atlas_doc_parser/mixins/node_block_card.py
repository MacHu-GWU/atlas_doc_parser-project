# -*- coding: utf-8 -*-

"""
Mixin for ADF Node: blockCard
"""

import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from ..nodes.node_block_card import NodeBlockCard


class NodeBlockCardMixin:
    def to_markdown(
        self: "NodeBlockCard",
        ignore_error: bool = False
    ) -> str:
        if isinstance(self.attrs.url, str):
            return f"\n[{self.attrs.url}]({self.attrs.url})\n"
        else:
            raise NotImplementedError