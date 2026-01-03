# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_nested_expand import NodeNestedExpand

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeNestedExpand:
    def test_node_nested_expand_basic(self):
        node = AdfSampleEnum.node_nested_expand_in_expand.test(NodeNestedExpand)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_nested_expand",
        preview=False,
    )
