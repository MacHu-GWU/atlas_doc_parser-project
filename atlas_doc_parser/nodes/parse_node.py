# -*- coding: utf-8 -*-

"""
Auto-generated ADF Parser

This module provides functions to parse ADF JSON into Python objects.
"""

import typing as T

from ..type_hint import T_DATA
from ..type_enum import TypeEnum

if T.TYPE_CHECKING:  # pragma: no cover
    from ..mark_or_node import T_NODE

# =============================================================================
# Node imports
# =============================================================================
from .node_text import NodeText


# =============================================================================
# Node registry
# =============================================================================
_node_type_to_class_mapping = {
    TypeEnum.text.value: NodeText,
}


def parse_node(dct: T_DATA) -> "T_NODE":
    """Parse a node dictionary into a Node object."""
    type_ = dct["type"]
    klass = _node_type_to_class_mapping[type_]
    return klass.from_dict(dct)
