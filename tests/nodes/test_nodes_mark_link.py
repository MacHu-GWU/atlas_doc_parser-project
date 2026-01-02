# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.mark_link import MarkLink

from atlas_doc_parser.tests import check_seder
from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestSeder:
    def test_link_mark_with_title_and_href(self):
        data = AdfSampleEnum.mark_link.data
        mark = MarkLink.from_dict(data)
        check_seder(mark)


class TestToMarkdown:
    def test_link_mark_without_title_uses_text(self):
        data = {
            "type": "link",
            "attrs": {"href": "http://atlassian.com", "title": "Atlassian"},
        }
        mark = MarkLink.from_dict(data)
        assert mark.to_markdown("Atlassian") == "[Atlassian](http://atlassian.com)"

    def test_link_mark_missing_required_attrs_raises(self):
        data = {"type": "link", "attrs": {"href": "http://example.com"}}
        mark = MarkLink.from_dict(data)
        assert mark.to_markdown("Click here") == "[Click here](http://example.com)"

    def test_link_mark_with_special_chars_in_url(self):

        data = {
            "type": "link",
            "attrs": {
                "href": "http://example.com/path?param=value&other=123",
                "title": "Complex URL",
            },
        }
        mark = MarkLink.from_dict(data)
        assert (
            mark.to_markdown("Special Link")
            == "[Complex URL](http://example.com/path?param=value&other=123)"
        )


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_cov_test

    run_cov_test(
        __file__,
        "atlas_doc_parser.nodes.mark_link",
        preview=False,
    )
