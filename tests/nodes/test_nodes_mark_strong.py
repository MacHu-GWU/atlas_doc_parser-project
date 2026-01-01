# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.mark_strong import MarkStrong

from atlas_doc_parser.tests import check_seder
from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestSeder:
    def test_basic_strong_mark(self):
        data = AdfSampleEnum.mark_strong.data
        mark = MarkStrong.from_dict(data)
        check_seder(mark)


class TestToMarkdown:
    def test(self):
        data = AdfSampleEnum.mark_strong.data
        mark = MarkStrong.from_dict(data)

        valid_text = [
            "Hello world",
            "Hello * World ** !",
            "  Hello  World  ",
        ]
        for before in valid_text:
            assert mark.to_markdown(before) == f"**{before}**"

        invalid_text = [
            "",
            "  ",
        ]
        for before in invalid_text:
            assert mark.to_markdown(before) == before


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.mark_strong",
        preview=False,
    )
