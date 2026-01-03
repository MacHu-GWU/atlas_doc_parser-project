# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_text import NodeText

from atlas_doc_parser.tests.data.samples import AdfSampleEnum, AdfSample


class TestNodeText:
    def test_node_text_basic(self):
        node = AdfSampleEnum.node_text.test(NodeText)

    def test_node_text_with_strong_emphasis(self):
        node = AdfSampleEnum.node_strong_text.test(NodeText)

    def test_node_text_with_italic(self):
        node = AdfSampleEnum.node_italic_text.test(NodeText)

    def test_node_text_with_underline(self):
        node = AdfSampleEnum.node_underline_text.test(NodeText)

    def test_node_text_with_strikethrough(self):
        node = AdfSampleEnum.node_strike_text.test(NodeText)

    def test_node_text_with_code_mark(self):
        node = AdfSampleEnum.mark_inline_code_text.test(NodeText)

    def test_node_text_with_subsup(self):
        node = AdfSampleEnum.node_sub_text.test(NodeText)
        node = AdfSampleEnum.node_sup_text.test(NodeText)

    def test_node_text_with_text_color(self):
        node = AdfSampleEnum.node_colored_text.test(NodeText)

    def test_node_text_with_background_color(self):
        node = AdfSampleEnum.node_background_colored_text.test(NodeText)

    def test_node_text_with_titled_hyperlink(self):
        data = {
            "text": "Atlassian",
            "type": "text",
            "marks": [
                {
                    "type": "link",
                    "attrs": {
                        "href": "http://atlassian.com",
                        "title": "Atlassian",
                    },
                }
            ],
        }
        node = NodeText.from_dict(data)
        md = "[Atlassian](http://atlassian.com)"
        AdfSample.test_node_or_mark(node, md)

    def test_node_text_with_url_hyperlink(self):
        data = {
            "text": "Atlassian",
            "type": "text",
            "marks": [
                {
                    "type": "link",
                    "attrs": {
                        "href": "http://atlassian.com",
                    },
                },
            ],
        }
        node = NodeText.from_dict(data)
        md = "[Atlassian](http://atlassian.com)"
        AdfSample.test_node_or_mark(node, md)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_text",
        preview=False,
    )
