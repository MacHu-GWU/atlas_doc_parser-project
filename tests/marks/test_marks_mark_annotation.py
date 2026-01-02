# -*- coding: utf-8 -*-

from atlas_doc_parser.marks.mark_annotation import MarkAnnotation

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestMarkAnnotation:
    def test_basic_strong_mark(self):
        mark = AdfSampleEnum.mark_annotation.test(MarkAnnotation)

        valid_text = [
            "Hello world",
            "",
            "  ",
        ]
        for before in valid_text:
            assert mark.to_markdown(before) == before


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.marks.mark_annotation",
        preview=False,
    )
