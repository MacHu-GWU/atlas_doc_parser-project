# -*- coding: utf-8 -*-

"""
CLI to fetch ADF JSON from Confluence pages.

Usage::

    .venv/bin/python .claude/skills/adf-json-example/scripts/adf_json_example_cli.py get_example "<url>"
"""

import json

import fire

from atlas_doc_parser.tests.data.samples import PageSample


class Command:
    """ADF JSON example commands."""

    def get_example(self, confluence_url: str) -> None:
        """
        Fetch and print ADF JSON from a Confluence page.

        :param confluence_url: Full Confluence page URL.
        """
        page_sample = PageSample(name="tmp", url=confluence_url)
        print(json.dumps(page_sample.adf, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    fire.Fire(Command)
