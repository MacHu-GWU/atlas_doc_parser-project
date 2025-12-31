# -*- coding: utf-8 -*-

import typing as T
from ..type_hint import T_DATA

if T.TYPE_CHECKING:  # pragma: no cover
    from .base import T_MARK, T_NODE

_mark_type_to_class_mapping = {}


def parse_mark(dct: T_DATA) -> "T_MARK":
    # print("--- parse_mark() called")  # for debug only
    # print(f"{dct = }")  # for debug only
    type_ = dct["type"]
    klass = _mark_type_to_class_mapping[type_]
    # print(f"{klass = }")  # for debug only
    return klass.from_dict(dct)


_node_type_to_class_mapping = {}


def parse_node(dct: T_DATA) -> "T_NODE":
    # print("--- parse_node() called")  # for debug only
    # print(f"{dct = }")  # for debug only
    type_ = dct["type"]
    klass = _node_type_to_class_mapping[type_]
    # print(f"{klass = }")  # for debug only
    return klass.from_dict(dct)
