# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_task_list import NodeTaskList

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TesNodeTaskList:
    def test_task_list_node_basic(self):
        node = AdfSampleEnum.node_task_list.test(NodeTaskList)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_task_list",
        preview=False,
    )
