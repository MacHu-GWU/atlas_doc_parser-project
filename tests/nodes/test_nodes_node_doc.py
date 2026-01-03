# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_doc import NodeDoc

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeDoc:
    def test_node_doc_basic(self):
        node = AdfSampleEnum.node_doc.test(NodeDoc)

    def test_node_doc_with_unimplemented_model(self):
        node = AdfSampleEnum.node_doc_with_unimplemented_model.test(NodeDoc)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_doc",
        preview=False,
    )
