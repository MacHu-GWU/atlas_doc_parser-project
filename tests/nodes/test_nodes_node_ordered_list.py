# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_ordered_list import NodeOrderedList

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeOrderedList:
    def test_node_ordered_list_basic(self):
        node = AdfSampleEnum.node_ordered_list.test(NodeOrderedList)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_bullet_list",
        preview=False,
    )
