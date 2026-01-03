# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_date import NodeDate

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeDate:
    def test_node_date_basic(self):
        node = AdfSampleEnum.node_date.test(NodeDate)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_date",
        preview=False,
    )
