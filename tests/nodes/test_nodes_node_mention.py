# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_mention import NodeMention

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeMention:
    def test_node_mention_basic(self):
        node = AdfSampleEnum.node_mention.test(NodeMention)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_mention",
        preview=False,
    )
