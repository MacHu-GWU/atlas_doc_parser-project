# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_rule import NodeRule

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeRule:
    def test_node_rule_basic(self):
        node = AdfSampleEnum.node_rule.test(NodeRule)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_rule",
        preview=False,
    )
