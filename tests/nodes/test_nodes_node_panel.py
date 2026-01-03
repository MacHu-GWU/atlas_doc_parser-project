# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_panel import NodePanel

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodePanel:
    def test_node_panel_basic(self):
        node = AdfSampleEnum.node_panel.test(NodePanel)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_panel",
        preview=False,
    )
