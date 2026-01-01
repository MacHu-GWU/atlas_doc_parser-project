# -*- coding: utf-8 -*-

"""
ADF Test Samples Module

Provides sample ADF node/mark data extracted from real Confluence pages for
testing serialization and deserialization of ADF dataclasses.

Two-layer architecture:
    - :class:`PageSample`: Represents a Confluence page with cached ADF content.
    - :class:`AdfSample`: Extracts a specific node/mark from a PageSample via JMESPath.

This design allows multiple samples to be extracted from the same page
(e.g., both ``mark_sub`` and ``mark_sup`` from a single "subsup" page).
"""

import json
import dataclasses
from functools import cached_property

import jmespath
from sanhe_confluence_sdk.methods.page.get_page import (
    GetPageRequestPathParams,
    GetPageRequestQueryParams,
    GetPageRequest,
)

from .client import client
from ...paths import path_enum


@dataclasses.dataclass
class PageSample:
    """
    A Confluence page as a source of ADF test samples.

    Fetches and caches the full ADF content of a Confluence page. Use
    :meth:`get_sample` to extract specific nodes/marks via JMESPath.

    Attributes:
        name: Unique identifier, used as the cache filename.
        url: Confluence page URL (used to extract page_id).

    Example:
        >>> page = PageSample(name="mark_subsup", url="...")
        >>> mark_sub = page.get_sample(jpath="content[0].content[1].marks[1]")
        >>> mark_sup = page.get_sample(jpath="content[0].content[3].marks[1]")
    """

    name: str
    url: str

    @property
    def page_id(self) -> int:
        """Extract page ID from URL (second-to-last path segment)."""
        return int(self.url.split("/")[-2])

    @property
    def path(self):
        """Local cache file path: {test_pages_dir}/{name}.json"""
        return path_enum.dir_adf_samples / f"{self.name}.json"

    @cached_property
    def adf(self) -> dict:
        """
        Full ADF content of the source Confluence page.

        Loads from local cache if available, otherwise fetches from API and caches.
        """
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

    def get_sample(self, jpath: str) -> "AdfSample":
        """Create an AdfSample that extracts a specific node/mark from this page."""
        return AdfSample(page=self, jpath=jpath)


@dataclasses.dataclass
class AdfSample:
    """
    A specific ADF node or mark extracted from a PageSample.

    Attributes:
        page: The source PageSample containing the full ADF.
        jpath: JMESPath expression to locate the target node/mark.

    Example:
        >>> sample = AdfSampleEnum.mark_strong
        >>> sample.data  # Returns {'type': 'strong'}
    """

    page: PageSample
    jpath: str

    @cached_property
    def data(self) -> dict:
        """The extracted ADF node/mark JSON, located via jpath from the page's ADF."""
        return jmespath.search(self.jpath, self.page.adf)


class AdfSampleEnum:
    """
    Registry of ADF test samples for nodes and marks.

    Each public attribute is an :class:`AdfSample` that extracts a specific ADF
    element from a Confluence page using JMESPath. Use ``_page`` prefix for
    intermediate PageSample objects when extracting multiple samples from one page.

    Naming Conventions:
        - ``mark_*``: Mark type samples (text formatting)
        - ``node_*``: Node type samples (block elements)
        - ``_page*``: Internal PageSample for multi-sample extraction

    Example:
        >>> from atlas_doc_parser.tests.data.samples import AdfSampleEnum
        >>> AdfSampleEnum.mark_strong.data
        {'type': 'strong'}
    """

    mark_background_color = PageSample(
        name="mark_background_color",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558524/Mark+-+backgroundColor",
    ).get_sample(jpath="content[0].content[1].marks[1]")
    mark_code = PageSample(
        name="mark_code",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049333/Mark+-+code",
    ).get_sample(jpath="content[0].content[1].marks[1]")
    mark_em = PageSample(
        name="mark_em",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049341/Mark+-+em",
    ).get_sample(jpath="content[0].content[1].marks[1]")
    mark_link = PageSample(
        name="mark_link",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082109/Mark+-+link",
    ).get_sample(jpath="content[0].content[1].marks[1]")
    mark_strike = PageSample(
        name="mark_strike",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558555/Mark+-+strike",
    ).get_sample(jpath="content[0].content[1].marks[1]")
    mark_strong = PageSample(
        name="mark_strong",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049306/Mark+-+strong",
    ).get_sample(jpath="content[0].content[1].marks[1]")

    _page = PageSample(
        name="mark_subsup",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558564/Mark+-+subsup",
    )
    mark_sub = _page.get_sample(jpath="content[0].content[1].marks[1]")
    mark_sup = _page.get_sample(jpath="content[0].content[3].marks[1]")

    mark_text_color = PageSample(
        name="mark_text_color",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558571/Mark+-+textColor",
    ).get_sample(jpath="content[0].content[1].marks[1]")
    mark_underline = PageSample(
        name="mark_underline",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082132/Mark+-+underline",
    ).get_sample(jpath="content[0].content[1].marks[1]")
    # node_block_quote = AdfSample(
    #     name="node_block_quote",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492407/Node+-+blockquote",
    # )
    # node_bullet_list = AdfSample(
    #     name="node_bullet_list",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082139/Node+-+bulletList",
    # )
    # node_code_block = AdfSample(
    #     name="node_code_block",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049370/Node+-+codeBlock",
    # )
    # node_date = AdfSample(
    #     name="node_date",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082153/Node+-+date",
    # )
    # node_emoji = AdfSample(
    #     name="node_emoji",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049377/Node+-+emoji",
    # )
    # node_heading = AdfSample(
    #     name="node_heading",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492448/Node+-+heading",
    # )
    # node_inline_card = AdfSample(
    #     name="node_inline_card",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492455/Node+-+inlineCard",
    # )
    # node_mention = AdfSample(
    #     name="node_mention",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492462/Node+-+mention",
    # )
    # node_ordered_list = AdfSample(
    #     name="node_ordered_list",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558633/Node+-+orderedList",
    # )
    # node_panel = AdfSample(
    #     name="node_panel",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558640/Node+-+panel",
    # )
    # node_paragraph = AdfSample(
    #     name="node_paragraph",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082201/Node+-+paragraph",
    # )
    # node_rule = AdfSample(
    #     name="node_rule",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558648/Node+-+rule",
    # )
    # node_status = AdfSample(
    #     name="node_status",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049423/Node+-+status",
    # )
    # node_table = AdfSample(
    #     name="node_table",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082217/Node+-+table",
    # )
    # node_text = AdfSample(
    #     name="node_text",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049439/Node+-+text",
    # )
