# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_table import NodeTable

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeTable:
    def test_node_table_basic(self):
        node = AdfSampleEnum.node_table_simple.test(NodeTable)
        node = AdfSampleEnum.node_table_complicated.test(NodeTable)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_table",
        preview=False,
    )
