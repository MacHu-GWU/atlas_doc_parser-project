# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_decision_list import NodeDecisionList

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeDecisionList:
    def test_task_list_node_basic(self):
        node = AdfSampleEnum.node_decision_list.test(NodeDecisionList)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_decision_list",
        preview=False,
    )
