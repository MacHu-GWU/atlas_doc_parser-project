# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_hint import T_DATA
from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeBlockCardAttrsDatasourceView(Base):
    """
    A view configuration for a datasource.

    :param type: Required. The view type identifier.
    :param properties: Optional. Additional view properties.
    """

    type: str = OPT
    properties: T_DATA = OPT


@dataclasses.dataclass(frozen=True)
class NodeBlockCardAttrsDatasource(Base):
    """
    Datasource configuration for :class:`NodeBlockCardAttrs`.

    :param id: Required. The datasource identifier.
    :param parameters: Required. Datasource parameters (structure varies).
    :param views: Required. Array of view configurations (minimum 1 item).
    """

    id: str = OPT
    parameters: T_DATA = OPT
    views: list[NodeBlockCardAttrsDatasourceView] = OPT


@dataclasses.dataclass(frozen=True)
class NodeBlockCardAttrs(Base):
    """
    Attributes for :class:`NodeBlockCard`.

    The blockCard attrs supports three variants (anyOf):

    1. **Datasource variant** (requires ``datasource``):
       - ``datasource``: Datasource configuration
       - ``url``: Optional URL
       - ``width``: Optional width
       - ``layout``: Optional layout mode

    2. **URL variant** (requires ``url``):
       - ``url``: The URL for the smart link

    3. **Data variant** (requires ``data``):
       - ``data``: Inline data object

    All variants may include ``localId``.

    :param url: Optional. The URL for the smart link.
    :param localId: Optional. A local unique identifier for the node.
    :param datasource: Optional. Datasource configuration for data-driven cards.
    :param width: Optional. Width of the card (datasource variant only).
    :param layout: Optional. Layout mode: wide, full-width, center, wrap-right,
        wrap-left, align-end, align-start.
    :param data: Optional. Inline data object (data variant only).
    """

    url: str = OPT
    localId: str = OPT
    datasource: NodeBlockCardAttrsDatasource = OPT
    width: float = OPT
    layout: str = OPT
    data: T_DATA = OPT


@dataclasses.dataclass(frozen=True)
class NodeBlockCard(BaseNode):
    """
    A block-level smart link card.

    The blockCard node displays a rich preview of linked content as a
    standalone block element. It can be configured with a URL, datasource,
    or inline data.

    This is a top-level block node that renders as a card with metadata
    from the linked resource (title, description, icon, etc.).
    """

    type: str = TypeEnum.blockCard.value
    attrs: NodeBlockCardAttrs = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        if isinstance(self.attrs.url, str):
            return f"\n[{self.attrs.url}]({self.attrs.url})\n"
        else:
            raise NotImplementedError
