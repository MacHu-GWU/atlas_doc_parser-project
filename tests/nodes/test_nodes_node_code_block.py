# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_code_block import NodeCodeBlock

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeCodeBlock:
    def test_node_code_block_basic(self):
        node = AdfSampleEnum.node_code_block.test(NodeCodeBlock)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_code_block",
        preview=False,
    )
