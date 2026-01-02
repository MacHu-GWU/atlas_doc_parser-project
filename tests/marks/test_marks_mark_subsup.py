# -*- coding: utf-8 -*-

from atlas_doc_parser.marks.mark_subsup import MarkSubsup

from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestMarkSubsup:
    def test_basic_sub_mark(self):
        mark = AdfSampleEnum.mark_sub.test(MarkSubsup)

    def test_basic_sup_mark(self):
        mark = AdfSampleEnum.mark_sup.test(MarkSubsup)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.marks.mark_subsup",
        preview=False,
    )
