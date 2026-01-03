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

import typing as T
import json
import textwrap
import dataclasses
from functools import cached_property

import jmespath
from sanhe_confluence_sdk.methods.page.get_page import (
    GetPageRequestPathParams,
    GetPageRequestQueryParams,
    GetPageRequest,
)

from ...mark_or_node import T_BASE, T_MARK, T_NODE, BaseMark, BaseNode
from ...paths import path_enum
from ..helper import check_seder, check_markdown
from .client import client


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

    def get_sample(
        self,
        jpath: str,
        md: str | None = None,
    ) -> "AdfSample":
        """Create an AdfSample that extracts a specific node/mark from this page."""
        return AdfSample(page=self, jpath=jpath, md=md)


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
    md: str | None

    @cached_property
    def data(self) -> dict:
        """The extracted ADF node/mark JSON, located via jpath from the page's ADF."""
        return jmespath.search(self.jpath, self.page.adf)

    @cached_property
    def markdown(self) -> str | None:
        if self.md is None:
            return self.md
        else:
            return textwrap.dedent(self.md)

    def get_inst(self, klass: T.Type["T_BASE"]) -> "T_BASE":
        """
        Get the deserialized instance of the extracted node/mark.
        """
        return klass.from_dict(self.data)

    @staticmethod
    def test_node_or_mark(
        node_or_mark: T.Union["T_MARK", "T_NODE"],
        markdown: str | None = None,
    ):
        """
        A test helper method.

        Test serialization/deserialization and Markdown conversion.
        """
        check_seder(inst=node_or_mark)
        if isinstance(node_or_mark, BaseNode) and markdown is not None:
            check_markdown(
                node=node_or_mark,
                expected=markdown,
            )

    def test(self, klass: T.Type["T_BASE"]) -> "T_BASE":
        """
        A test helper method.

        Test serialization/deserialization and Markdown conversion.
        """
        node_or_mark = self.get_inst(klass)
        self.test_node_or_mark(node_or_mark, self.markdown)
        return node_or_mark


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

    .. seealso::

        https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082078/atlas_doc_parser+-+Single+Mark+or+Node+Test
    """
    # --------------------------------------------------------------------------
    # Mark
    # --------------------------------------------------------------------------
    _page = PageSample(
        name="mark_background_color",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558524/Mark+-+backgroundColor",
    )
    mark_background_color = _page.get_sample(jpath="content[0].content[1].marks[1]")
    node_background_colored_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="backgroundColor",
    )

    mark_annotation = _page.get_sample(jpath="content[0].content[1].marks[0]")

    _page = PageSample(
        name="mark_code",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049333/Mark+-+code",
    )
    mark_code = _page.get_sample(jpath="content[0].content[1].marks[1]")
    mark_inline_code_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="`` code ``",
    )

    _page = PageSample(
        name="mark_em",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049341/Mark+-+em",
    )
    mark_em = _page.get_sample(jpath="content[0].content[1].marks[1]")
    node_italic_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="*italic*",
    )

    mark_link = PageSample(
        name="mark_link",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082109/Mark+-+link",
    ).get_sample(jpath="content[0].content[1].marks[1]")

    _page = PageSample(
        name="mark_strike",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558555/Mark+-+strike",
    )
    mark_strike = _page.get_sample(jpath="content[0].content[1].marks[1]")
    node_strike_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="~~strike~~",
    )

    _page = PageSample(
        name="mark_strong",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049306/Mark+-+strong",
    )
    mark_strong = _page.get_sample(jpath="content[0].content[1].marks[1]")
    node_strong_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="**strong**",
    )

    _page = PageSample(
        name="mark_subsup",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558564/Mark+-+subsup",
    )
    mark_sub = _page.get_sample(jpath="content[0].content[1].marks[1]")
    mark_sup = _page.get_sample(jpath="content[0].content[3].marks[1]")
    node_sub_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="sub",
    )
    node_sup_text = _page.get_sample(
        jpath="content[0].content[3]",
        md="sup",
    )

    _page = PageSample(
        name="mark_text_color",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558571/Mark+-+textColor",
    )
    mark_text_color = _page.get_sample(jpath="content[0].content[1].marks[1]")
    node_colored_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="colored",
    )

    _page = PageSample(
        name="mark_underline",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082132/Mark+-+underline",
    )
    mark_underline = _page.get_sample(jpath="content[0].content[1].marks[1]")
    node_underline_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="underline",
    )

    # --------------------------------------------------------------------------
    # Node
    # --------------------------------------------------------------------------
    node_text = PageSample(
        name="node_text",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049439/Node+-+text",
    ).get_sample(
        jpath="content[0].content[0]",
        md="this is a text.",
    )
    node_rule = PageSample(
        name="node_rule",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558648/Node+-+rule",
    ).get_sample(
        jpath="content[0]",
        md="\n\n---\n\n",
    )
    node_bullet_list = PageSample(
        name="node_bullet_list",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082139/Node+-+bulletList",
    ).get_sample(
        jpath="content[0]",
        md="""
            - item **1**
                - item **1.1**
                    - item **1.1.1**
            - item 2
                - item 2.1
                    - item 2.1.1
            - item 3
                - item 3.1
                    - item 3.1.1
            """,
    )
    node_ordered_list = PageSample(
        name="node_ordered_list",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558633/Node+-+orderedList",
    ).get_sample(
        jpath="content[0]",
        md="""
            1. item **1**
                1. item **1.1**
                    1. item **1.1.1**
            2. item 2
                1. item 2.1
                    1. item 2.1.1
            3. item 3
                1. item 3.1
                    1. item 3.1.1
            """,
    )
    node_task_list = PageSample(
        name="node_task_list",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653885443/Node+-+taskList",
    ).get_sample(
        jpath="content[0]",
        md="""
            - [x] item **1**
                - [x] item **1.1**
                    - [x] item **1.1.1**
            - [ ] item 2
                - [x] item 2.1
                    - [ ] item 2.1.1
            - [ ] item 3
                - [ ] item 3.1
                    - [x] item 3.1.1
            """,
    )
    node_decision_list = PageSample(
        name="node_decision_list",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654147585/Node+-+decisionList",
    ).get_sample(
        jpath="content[0]",
        md="""
            - [x] item **1**
                - [x] item **1.1**
                    - [x] item **1.1.1**
            - [ ] item 2
                - [x] item 2.1
                    - [ ] item 2.1.1
            - [ ] item 3
                - [ ] item 3.1
                    - [x] item 3.1.1
            """,
    )

    node_block_quote = PageSample(
        name="node_block_quote",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492407/Node+-+blockquote",
    ).get_sample(
        jpath="content[0]",
        md="""
        > Alice says:
        > 
        > Just do it!
        """,
    )

    node_code_block = PageSample(
        name="node_code_block",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049370/Node+-+codeBlock",
    ).get_sample(jpath="content[0]")
    node_date = PageSample(
        name="node_date",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082153/Node+-+date",
    ).get_sample(jpath="content[0].content[1]")
    node_emoji = PageSample(
        name="node_emoji",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049377/Node+-+emoji",
    ).get_sample(jpath="content[0].content[1]")
    node_heading = PageSample(
        name="node_heading",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492448/Node+-+heading",
    ).get_sample(jpath="content[0]")
    node_inline_card = PageSample(
        name="node_inline_card",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492455/Node+-+inlineCard",
    ).get_sample(jpath="content[0]")
    node_mention = PageSample(
        name="node_mention",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653492462/Node+-+mention",
    ).get_sample(jpath="content[0].content[0]")

    node_panel = PageSample(
        name="node_panel",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558640/Node+-+panel",
    ).get_sample(jpath="content[0]")

    node_paragraph = PageSample(
        name="node_paragraph",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082201/Node+-+paragraph",
    ).get_sample(
        jpath="content[0]",
        md="""
        This is a **bolded text**, do you see that? This is a *italic text*, do you see that? This is a underline, do you see that? This is a ~~strike through~~, do you see that? This is a ***~~bolded itlic strike through and underline~~***, do you see that? This is a subscript, do you see that? This is a superscript, do you see that? This text has color, do you see that? This text has background, do you see that? Note that you can not do Text color and Background color at the same time. This line has code `` a = 1 + 2 ``**.**
        """,
    )

    node_status = PageSample(
        name="node_status",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049423/Node+-+status",
    ).get_sample(jpath="content[0].content[0]")
    node_table = PageSample(
        name="node_table",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082217/Node+-+table",
    ).get_sample(jpath="content[0]")

