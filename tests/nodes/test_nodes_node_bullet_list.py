# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_bullet_list import NodeBulletList

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeBulletList:
    def test_node_bullet_list_basic(self):
        node = AdfSampleEnum.node_bullet_list.test(NodeBulletList)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_bullet_list",
        preview=False,
    )
