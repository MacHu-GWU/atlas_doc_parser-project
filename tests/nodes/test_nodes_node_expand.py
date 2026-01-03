# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_expand import NodeExpand

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeExpand:
    def test_node_expand_basic(self):
        node = AdfSampleEnum.node_expand.test(NodeExpand)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_expand",
        preview=False,
    )
