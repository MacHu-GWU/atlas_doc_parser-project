# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_ordered_list import NodeOrderedList

from atlas_doc_parser.tests.data.samples import AdfSampleEnum, AdfSample


def _list_item(text: str, *children: dict) -> dict:
    return {
        "type": "listItem",
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": text}]},
            *children,
        ],
    }


class TestNodeOrderedList:
    def test_node_ordered_list_basic(self):
        node = AdfSampleEnum.node_ordered_list.test(NodeOrderedList)

    def test_node_ordered_list_without_attrs(self):
        # Jira omits "attrs" when the list starts at 1
        data = {
            "type": "orderedList",
            "content": [
                _list_item(
                    "item 1",
                    {
                        "type": "orderedList",
                        "content": [_list_item("item 1.1")],
                    },
                ),
                _list_item("item 2"),
            ],
        }
        node = NodeOrderedList.from_dict(data)
        md = "1. item 1\n    1. item 1.1\n2. item 2"
        AdfSample.test_node_or_mark(node, md)

    def test_node_ordered_list_with_custom_order(self):
        data = {
            "type": "orderedList",
            "attrs": {"order": 5},
            "content": [_list_item("item 5"), _list_item("item 6")],
        }
        node = NodeOrderedList.from_dict(data)
        md = "5. item 5\n6. item 6"
        AdfSample.test_node_or_mark(node, md)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_bullet_list",
        preview=False,
    )
