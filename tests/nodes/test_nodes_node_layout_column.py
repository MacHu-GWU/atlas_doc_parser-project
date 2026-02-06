# -*- coding: utf-8 -*-

import json
from pathlib import Path

from atlas_doc_parser.nodes.node_layout_column import NodeLayoutColumn


dir_adf_samples = Path(__file__).parent.parent / "adf_samples"


class TestNodeLayoutColumn:
    def test_from_dict_and_seder(self):
        with open(dir_adf_samples / "node_layout_column.json") as f:
            data = json.load(f)
        node = NodeLayoutColumn.from_dict(data)
        assert node.type == "layoutColumn"
        assert node.attrs.width == 50.0
        # Roundtrip serialization
        assert node.to_dict() == data

    def test_to_markdown(self):
        with open(dir_adf_samples / "node_layout_column.json") as f:
            data = json.load(f)
        node = NodeLayoutColumn.from_dict(data)
        md = node.to_markdown().strip()
        assert md == "Column content"

    def test_without_attrs(self):
        data = {
            "type": "layoutColumn",
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": "No width specified"}],
                }
            ],
        }
        node = NodeLayoutColumn.from_dict(data)
        assert node.to_markdown().strip() == "No width specified"
