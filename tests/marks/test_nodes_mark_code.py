# -*- coding: utf-8 -*-

from atlas_doc_parser.marks.mark_code import MarkCode

import pytest
from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestSeder:
    def test_basic_code_mark(self):
        mark = AdfSampleEnum.mark_code.test(MarkCode)

        valid_text = [
            "print('hello')",
            "var x = `template string`",
            "def func():;    return True",
            "  code  ",
            "\tcode\t",
        ]
        for before in valid_text:
            assert mark.to_markdown(before) == f"`` {before} ``"

        empty_text = [
            "",
            "  ",
        ]
        for before in empty_text:
            assert mark.to_markdown(before) == before

        invalid_text = [
            "code\nmore code",
        ]
        for before in invalid_text:
            with pytest.raises(ValueError):
                mark.to_markdown(before)


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.marks.mark_code",
        preview=False,
    )
