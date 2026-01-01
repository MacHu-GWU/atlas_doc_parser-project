# -*- coding: utf-8 -*-

"""
Confluence Test Page Data Module

This module provides utilities for fetching and caching Confluence page content
in Atlassian Document Format (ADF) for testing purposes. It supports lazy-loading
of page data with local file caching to minimize API calls during test runs.

The cached JSON files are stored in the test data directory and can be committed
to version control for reproducible offline testing.
"""

import json
import dataclasses
from functools import cached_property

from sanhe_confluence_sdk.methods.page.get_page import (
    GetPageRequestPathParams,
    GetPageRequestQueryParams,
    GetPageRequest,
)

from .client import client
from ...paths import path_enum


@dataclasses.dataclass
class Page:
    name: str
    url: str

    @property
    def page_id(self) -> int:
        return int(self.url.split("/")[-2])

    @property
    def path(self):
        return path_enum.dir_test_pages / f"{self.name}.json"

    @cached_property
    def data(self) -> dict:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            request = GetPageRequest(
                path_params=GetPageRequestPathParams(id=self.page_id),
                query_params=GetPageRequestQueryParams(body_format="atlas_doc_format"),
            )
            response = request.sync(client)
            content = response.body.atlas_doc_format.value
            data = json.loads(content)
            content = json.dumps(data, indent=4, ensure_ascii=False)
            self.path.write_text(content, encoding="utf-8")
            return data


class PageEnum:
    """
    Example usage:

    >>> from atlas_doc_parser.tests.data.pages import PageEnum
    >>> PageEnum.mark_background_color.data
    {
        "type": "doc",
        "content": [
            {
                "type": "paragraph",
                "attrs": {
                    "localId": "b3ded07e-95a4-43ef-a10d-53033d802404"
                },
                "content": [
                    {
                        "text": "this is ",
                        "type": "text"
                    },
                    {
                        "text": "backgroundColor",
                        "type": "text",
                        "marks": [
                            {
                                "type": "annotation",
                                "attrs": {
                                    "annotationType": "inlineComment",
                                    "id": "91ea44b3-4301-4fc3-be59-73c8968268df"
                                }
                            },
                            {
                                "type": "backgroundColor",
                                "attrs": {
                                    "color": "#fedec8"
                                }
                            }
                        ]
                    },
                    {
                        "text": " text.",
                        "type": "text"
                    }
                ]
            }
        ],
        "version": 1
    }
    """
    mark_background_color = Page(
        name="mark_background_color",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558524/Mark+-+backgroundColor"
    )
    mark_code = Page(
        name="mark_code",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049333/Mark+-+code",
    )
    mark_em = Page(
        name="mark_em",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049341/Mark+-+em",
    )
    mark_link = Page(
        name="mark_link",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082109/Mark+-+link",
    )
    mark_strike = Page(
        name="mark_strike",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558555/Mark+-+strike",
    )
    mark_strong = Page(
        name="mark_strong",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049306/Mark+-+strong",
    )
    mark_subsup = Page(
        name="mark_subsup",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558564/Mark+-+subsup",
    )
    mark_text_color = Page(
        name="mark_text_color",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558571/Mark+-+textColor",
    )
    mark_underline = Page(
        name="mark_underline",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082132/Mark+-+underline",
    )
    node_block_quote = Page(
        name="node_block_quote",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492407/Node+-+blockquote",
    )
    node_bullet_list = Page(
        name="node_bullet_list",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082139/Node+-+bulletList",
    )
    node_code_block = Page(
        name="node_code_block",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049370/Node+-+codeBlock",
    )
    node_date = Page(
        name="node_date",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082153/Node+-+date",
    )
    node_emoji = Page(
        name="node_emoji",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049377/Node+-+emoji",
    )
    node_heading = Page(
        name="node_heading",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492448/Node+-+heading",
    )
    node_inline_card = Page(
        name="node_inline_card",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492455/Node+-+inlineCard",
    )
    node_mention = Page(
        name="node_mention",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492462/Node+-+mention",
    )
    node_ordered_list = Page(
        name="node_ordered_list",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558633/Node+-+orderedList",
    )
    node_panel = Page(
        name="node_panel",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558640/Node+-+panel",
    )
    node_paragraph = Page(
        name="node_paragraph",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082201/Node+-+paragraph",
    )
    node_rule = Page(
        name="node_rule",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558648/Node+-+rule",
    )
    node_status = Page(
        name="node_status",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049423/Node+-+status",
    )
    node_table = Page(
        name="node_table",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082217/Node+-+table",
    )
    node_text = Page(
        name="node_text",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049439/Node+-+text",
    )
