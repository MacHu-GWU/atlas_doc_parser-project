# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_embed_card import NodeEmbedCard

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeEmbedCard:
    def test_node_embed_card_basic(self):
        node = AdfSampleEnum.node_embed_card.test(NodeEmbedCard)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_embed_card",
        preview=False,
    )
