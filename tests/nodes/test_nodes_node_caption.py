# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_caption import NodeCaption

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeCaption:
    def test_node_caption_basic(self):
        node = AdfSampleEnum.node_caption_on_url_image.test(NodeCaption)
        node = AdfSampleEnum.node_caption_on_uploaded_image.test(NodeCaption)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_caption",
        preview=False,
    )
