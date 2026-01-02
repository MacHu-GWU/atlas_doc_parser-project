# -*- coding: utf-8 -*-

from atlas_doc_parser.marks.mark_strike import MarkStrike

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestSeder:
    def test_basic_strike_mark(self):
        mark = AdfSampleEnum.mark_strike.test(MarkStrike)

        valid_text = [
            "Hello world",
            "Hello ~ World ~~ !",
            "  Hello  World  ",
        ]
        for before in valid_text:
            assert mark.to_markdown(before) == f"~~{before}~~"

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
        "atlas_doc_parser.marks.mark_strike",
        preview=False,
    )
