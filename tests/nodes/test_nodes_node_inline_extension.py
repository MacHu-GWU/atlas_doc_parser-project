# -*- coding: utf-8 -*-

import json
from pathlib import Path

from atlas_doc_parser.nodes.node_inline_extension import NodeInlineExtension


dir_adf_samples = Path(__file__).parent.parent / "adf_samples"


class TestNodeInlineExtension:
    def test_from_dict_and_seder(self):
        with open(dir_adf_samples / "node_inline_extension.json") as f:
            data = json.load(f)
        node = NodeInlineExtension.from_dict(data)
        assert node.type == "inlineExtension"
        assert node.attrs.extensionKey == "pagetree"
        assert node.attrs.extensionType == "com.atlassian.confluence.macro.core"
        # Roundtrip serialization
        assert node.to_dict() == data

    def test_to_markdown(self):
        with open(dir_adf_samples / "node_inline_extension.json") as f:
            data = json.load(f)
        node = NodeInlineExtension.from_dict(data)
        md = node.to_markdown()
        assert md == "[Extension: com.atlassian.confluence.macro.core/pagetree]"

    def test_with_text_fallback(self):
        data = {
            "type": "inlineExtension",
            "attrs": {
                "extensionType": "com.example.app",
                "extensionKey": "my-macro",
                "text": "Fallback text",
            },
        }
        node = NodeInlineExtension.from_dict(data)
        assert node.to_markdown() == "[Extension: my-macro] Fallback text"
