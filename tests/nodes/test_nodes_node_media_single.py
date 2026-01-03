# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_media_single import NodeMediaSingle

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeMediaSingle:
    def test_node_media_single_basic(self):
        # fmt: off
        node = AdfSampleEnum.node_media_single_url_image.test(NodeMediaSingle)
        node = AdfSampleEnum.node_media_single_url_image_with_caption.test(NodeMediaSingle)
        node = AdfSampleEnum.node_media_single_url_image_with_alt_text.test(NodeMediaSingle)
        node = AdfSampleEnum.node_media_single_url_image_with_clickable_link.test(NodeMediaSingle)
        node = AdfSampleEnum.node_media_single_url_image_with_caption_and_clickable_link.test(NodeMediaSingle)
        node = AdfSampleEnum.node_media_single_uploaded_image.test(NodeMediaSingle)
        # fmt: on


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_media_single",
        preview=False,
    )
