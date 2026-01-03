# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_block_card import NodeBlockCard

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeBlockCard:
    def test_node_block_card_basic(self):
        node = AdfSampleEnum.node_block_card.test(NodeBlockCard)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_block_card",
        preview=False,
    )
