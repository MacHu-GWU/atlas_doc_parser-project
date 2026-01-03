# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_paragraph import NodeParagraph

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeHardBreak:
    def test_node_hard_break_basic(self):
        node = AdfSampleEnum.node_hard_break.test(NodeParagraph)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_hard_break",
        preview=False,
    )
