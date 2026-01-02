# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.mark_text_color import MarkTextColor

from atlas_doc_parser.tests import check_seder
from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestSeder:
    def test_basic_text_color_mark(self):
        data = AdfSampleEnum.mark_text_color.data
        mark = MarkTextColor.from_dict(data)
        check_seder(mark)


class TestToMarkdown:
    def test_case_1(self):
        pass


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.mark_text_color",
        preview=False,
    )
