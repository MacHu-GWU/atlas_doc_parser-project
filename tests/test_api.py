# -*- coding: utf-8 -*-

"""
Test that the api.py module exports all expected symbols.

This test verifies that:
1. Core classes and functions are exported
2. All mark and node classes are accessible
"""

from atlas_doc_parser import api


def test_core_exports():
    """Test that core classes and functions are exported."""
    # Exceptions
    _ = api.ParamError

    # Type enum
    _ = api.TypeEnum

    # Base classes
    _ = api.Base
    _ = api.BaseMarkOrNode
    _ = api.BaseMark
    _ = api.BaseNode

    # Type vars
    _ = api.T_MARK
    _ = api.T_NODE

    # Parse functions
    _ = api.parse_mark
    _ = api.parse_node


def test_marks_exported():
    """Test that all mark classes are exported."""
    # These are the marks we know should be exported
    # Test a few key ones to ensure the import mechanism works
    _ = api.MarkCode
    _ = api.MarkEm
    _ = api.MarkLink
    _ = api.MarkLinkAttrs
    _ = api.MarkStrong
    _ = api.MarkStrike


def test_nodes_exported():
    """Test that all node classes are exported."""
    # These are the nodes we know should be exported
    # Test a few key ones to ensure the import mechanism works
    _ = api.NodeDoc
    _ = api.NodeParagraph
    _ = api.NodeHeading
    _ = api.NodeHeadingAttrs
    _ = api.NodeText
    _ = api.NodeCodeBlock
    _ = api.NodeCodeBlockAttrs
    _ = api.NodeBlockquote
    _ = api.NodeBulletList
    _ = api.NodeOrderedList
    _ = api.NodeTable


def test_all_mark_classes_inherit_from_base():
    """Test that exported mark classes inherit from BaseMark."""
    import inspect

    for name in dir(api):
        if name.startswith("Mark") and not name.endswith("Attrs"):
            obj = getattr(api, name)
            if inspect.isclass(obj) and obj is not api.BaseMark:
                assert issubclass(obj, api.BaseMark), f"{name} should inherit from BaseMark"


def test_all_node_classes_inherit_from_base():
    """Test that exported node classes inherit from BaseNode."""
    import inspect

    for name in dir(api):
        # Skip Attrs classes (including nested ones like NodeBlockCardAttrsDatasource)
        if name.startswith("Node") and "Attrs" not in name:
            obj = getattr(api, name)
            if inspect.isclass(obj) and obj is not api.BaseNode:
                assert issubclass(obj, api.BaseNode), f"{name} should inherit from BaseNode"


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(__file__, "atlas_doc_parser.api", preview=False)
