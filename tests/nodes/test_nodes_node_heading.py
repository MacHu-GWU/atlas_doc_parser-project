# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_heading import NodeHeading

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeHeading:
    def test_node_heading_basic(self):
        node = AdfSampleEnum.node_heading_basic.test(NodeHeading)

    def test_node_header_with_background_color(self):
        node = AdfSampleEnum.node_header_1.test(NodeHeading)

    def test_node_header_with_colored_text(self):
        node = AdfSampleEnum.node_header_2.test(NodeHeading)

    def test_node_header_with_bold_text(self):
        node = AdfSampleEnum.node_header_3.test(NodeHeading)

    def test_node_header_with_strike_text(self):
        node = AdfSampleEnum.node_header_4.test(NodeHeading)

    def test_node_header_with_underline_text(self):
        node = AdfSampleEnum.node_header_5.test(NodeHeading)

    def test_node_header_with_hyperlink(self):
        node = AdfSampleEnum.node_header_6.test(NodeHeading)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_heading",
        preview=False,
    )
