# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.mark_strong import MarkStrong

from atlas_doc_parser.tests import check_seder
from atlas_doc_parser.tests.case import NodeCase, CaseEnum


class TestMarkStrong:
    def test_basic_strong_mark(self):
        """Test basic strong mark creation and markdown conversion."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        assert mark.to_markdown("Hello world") == "**Hello world**"

    def test_strong_mark_with_special_chars(self):
        """Test strong mark with text containing special characters."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        special_text = "Hello * World ** !"
        assert mark.to_markdown(special_text) == f"**{special_text}**"

    def test_strong_mark_with_empty_string(self):
        """Test strong mark with empty text."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        assert mark.to_markdown("") == "****"

    def test_strong_mark_preserves_whitespace(self):
        """Test strong mark with text containing various whitespace."""
        data = {"type": "strong"}
        mark = MarkStrong.from_dict(data)
        check_seder(mark)
        text_with_spaces = "  Hello  World  "
        assert mark.to_markdown(text_with_spaces) == f"**{text_with_spaces}**"


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.mark_strong",
        preview=False,
    )
