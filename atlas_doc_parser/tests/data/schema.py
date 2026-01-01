# -*- coding: utf-8 -*-

"""
Cached copy of the ADF JSON schema from http://go.atlassian.com/adf-json-schema.
Used for testing, code generation, and referencing ADF node/mark definitions.
"""

import json
from functools import cached_property

import httpx

from ...paths import path_enum


class AdfJsonSchema:
    """Lazy-loading accessor for the ADF JSON schema with local file caching."""

    @cached_property
    def data(self) -> dict:
        """Load schema from cache, or fetch from unpkg.com and cache locally."""
        path = path_enum.path_adf_json_schema
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            url = "https://unpkg.com/@atlaskit/adf-schema@51.5.4/dist/json-schema/v1/full.json"
            response = httpx.get(url)
            data = response.json()
            content = json.dumps(data, indent=2, ensure_ascii=False)
            path.write_text(content, encoding="utf-8")
            return data


adf_json_schema = AdfJsonSchema()
