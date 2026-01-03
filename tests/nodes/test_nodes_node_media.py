# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_media import NodeMedia

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeMedia:
    def test_node_media_basic(self):
        # fmt: off
        node = AdfSampleEnum.node_media_url_image.test(NodeMedia)
        node = AdfSampleEnum.node_media_url_image_with_caption.test(NodeMedia)
        node = AdfSampleEnum.node_media_url_image_with_alt_text.test(NodeMedia)
        node = AdfSampleEnum.node_media_url_image_with_clickable_link.test(NodeMedia)
        node = AdfSampleEnum.node_media_url_image_with_caption_and_clickable_link.test(NodeMedia)
        node = AdfSampleEnum.node_media_uploaded_image.test(NodeMedia)
        # fmt: on


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.node_media",
        preview=False,
    )
