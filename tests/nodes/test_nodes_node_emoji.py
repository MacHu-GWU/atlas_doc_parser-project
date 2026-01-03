# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_emoji import NodeEmoji

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeEmoji:
    def test_node_emoji_basic(self):
        node = AdfSampleEnum.node_emoji.test(NodeEmoji)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_emoji",
        preview=False,
    )
