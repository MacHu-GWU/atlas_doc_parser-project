# -*- coding: utf-8 -*-

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
    mark_background_color = Page(
        name="mark_background_color",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/653558524/Mark+-+backgroundColor"
    )
    mark_strong = Page(
        name="mark_strong",
        url="https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654049306/Mark+-+strong",
    )
