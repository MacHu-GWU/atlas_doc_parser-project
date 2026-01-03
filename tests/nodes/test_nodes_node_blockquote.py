# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_blockquote import NodeBlockquote

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeBlockquote:
    def test_node_blockquote_basic(self):
        node = AdfSampleEnum.node_blockquote.test(NodeBlockquote)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_blockquote",
        preview=False,
    )
