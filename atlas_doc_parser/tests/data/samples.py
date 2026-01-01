# -*- coding: utf-8 -*-

"""
ADF Test Samples Module

Provides sample ADF node/mark data extracted from real Confluence pages for
testing serialization and deserialization of ADF dataclasses.

Each sample references a Confluence page and uses JMESPath to extract the
specific ADF node or mark for testing.
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
class AdfSample:
    """
    A test sample containing a specific ADF node or mark extracted from a Confluence page.

    Attributes:
        name: Unique identifier, used as the cache filename.
        url: Confluence page URL (used to extract page_id).
        jpath: JMESPath expression to extract the target node/mark from the page's ADF.

    Example:
        >>> sample = AdfSample(name="mark_strong", url="...", jpath="content[0].content[0].marks[0]")
        >>> sample.data  # Returns the specific mark's JSON, not the whole page
    """

    name: str
    url: str
    jpath: str

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

    @cached_property
    def data(self) -> dict:
        """The extracted ADF node/mark JSON, located via jpath from the full ADF."""
        return jmespath.search(self.jpath, self.adf)


class AdfSampleEnum:
    """
    Registry of ADF test samples for nodes and marks.

    Each attribute is an :class:`AdfSample` that extracts a specific ADF element
    from a real Confluence page using JMESPath.

    Naming Conventions:
        - ``mark_*``: Mark type samples (text formatting)
        - ``node_*``: Node type samples (block elements)

    Example:
        >>> from atlas_doc_parser.tests.data.samples import AdfSampleEnum
        >>> AdfSampleEnum.mark_strong.data
        {'type': 'strong'}
    """
    # mark_background_color = AdfSample(
    #     name="mark_background_color",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558524/Mark+-+backgroundColor"
    # )
    # mark_code = AdfSample(
    #     name="mark_code",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049333/Mark+-+code",
    # )
    # mark_em = AdfSample(
    #     name="mark_em",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049341/Mark+-+em",
    # )
    # mark_link = AdfSample(
    #     name="mark_link",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082109/Mark+-+link",
    # )
    # mark_strike = AdfSample(
    #     name="mark_strike",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558555/Mark+-+strike",
    # )
    mark_strong = AdfSample(
        name="mark_strong",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049306/Mark+-+strong",
        jpath="content[0].content[0].marks[1]"
    )
    # mark_subsup = AdfSample(
    #     name="mark_subsup",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558564/Mark+-+subsup",
    # )
    # mark_text_color = AdfSample(
    #     name="mark_text_color",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558571/Mark+-+textColor",
    # )
    # mark_underline = AdfSample(
    #     name="mark_underline",
    #     url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082132/Mark+-+underline",
    # )
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
