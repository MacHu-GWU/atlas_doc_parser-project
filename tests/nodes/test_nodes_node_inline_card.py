# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_inline_card import NodeInlineCard

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeInlineCard:
    def test_node_inline_card_basic(self):
        node = AdfSampleEnum.node_inline_card.test(NodeInlineCard)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_inline_card",
        preview=False,
    )
