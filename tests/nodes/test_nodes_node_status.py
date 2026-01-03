# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_status import NodeStatus

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeStatus:
    def test_node_status_basic(self):
        node = AdfSampleEnum.node_status.test(NodeStatus)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_status",
        preview=False,
    )
