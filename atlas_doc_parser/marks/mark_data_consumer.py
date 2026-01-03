# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


@dataclasses.dataclass(frozen=True)
class MarkDataConsumerAttrs(Base):
    """
    Attributes for :class:`MarkDataConsumer`.

    :param sources: Required. An array of source identifiers (minimum 1 item).
    """

    sources: list[str]


@dataclasses.dataclass(frozen=True)
class MarkDataConsumer(BaseMark):
    """
    DataConsumer mark for ADF.

    The dataConsumer mark indicates that a node consumes data from specified
    sources. It contains an array of source identifiers.
    """

    type: str = TypeEnum.dataConsumer.value
    attrs: MarkDataConsumerAttrs = REQ
