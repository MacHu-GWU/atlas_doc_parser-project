# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.mark_subsup import MarkSubsup

from atlas_doc_parser.tests import check_seder
from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestSeder:
    def test_basic_sub_mark(self):
        data = AdfSampleEnum.mark_sub.data
        mark = MarkSubsup.from_dict(data)
        check_seder(mark)

    def test_basic_sup_mark(self):
        data = AdfSampleEnum.mark_sup.data
        mark = MarkSubsup.from_dict(data)
        check_seder(mark)


class TestToMarkdown:
    def test(self):
        pass


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.mark_subsup",
        preview=False,
    )
