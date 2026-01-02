# -*- coding: utf-8 -*-

from atlas_doc_parser.marks.mark_em import MarkEm

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestMarkEm:
    def test_basic_em_mark(self):
        mark = AdfSampleEnum.mark_em.test(MarkEm)

        valid_text = [
            "note",
            "\tcode\t",
        ]
        for before in valid_text:
            assert mark.to_markdown(before) == f"*{before}*"

        empty_text = [
            "",
            "  ",
        ]
        for before in empty_text:
            assert mark.to_markdown(before) == before


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.marks.mark_em",
        preview=False,
    )
