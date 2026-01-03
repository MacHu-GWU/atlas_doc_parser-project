# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_decision_list import NodeDecisionList
from atlas_doc_parser.nodes.node_decision_item import NodeDecisionItem

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeDecisionItem:
    def test_node_decision_item_simple(self):
        node = AdfSampleEnum.node_decision_item_simple.test(NodeDecisionItem)

    def test_node_decision_item_complex_1(self):
        node = AdfSampleEnum.node_decision_item_complex_1.test(NodeDecisionItem)

    def test_node_decision_item_complex_2(self):
        node = AdfSampleEnum.node_decision_item_complex_2.test(NodeDecisionItem)


class TestNodeDecisionList:
    def test_node_decision_list_basic(self):
        node = AdfSampleEnum.node_decision_list.test(NodeDecisionList)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_decision_list",
        preview=False,
    )
