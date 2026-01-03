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
NODE_TYPE_TO_CLASS_MAPPING = {
    TypeEnum.text.value: NodeText,
}


def parse_node(dct: T_DATA) -> "T_NODE":
    """Parse a node dictionary into a Node object."""
    type_ = dct["type"]
    klass = NODE_TYPE_TO_CLASS_MAPPING[type_]
    return klass.from_dict(dct)
