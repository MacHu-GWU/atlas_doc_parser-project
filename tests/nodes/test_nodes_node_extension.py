# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_extension import NodeExtension

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeExtension:
    def test_node_extension_basic(self):
        node = AdfSampleEnum.node_extension_draw_io_diagram.test(NodeExtension)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_extension",
        preview=False,
    )
