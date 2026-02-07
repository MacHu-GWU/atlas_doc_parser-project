# -*- coding: utf-8 -*-

import json
from pathlib import Path

from atlas_doc_parser.nodes.node_layout_section import NodeLayoutSection


dir_adf_samples = Path(__file__).parent.parent / "adf_samples"


class TestNodeLayoutSection:
    def test_from_dict_and_seder(self):
        with open(dir_adf_samples / "node_layout_section.json") as f:
            data = json.load(f)
        node = NodeLayoutSection.from_dict(data)
        assert node.type == "layoutSection"
        assert len(node.content) == 2
        # Roundtrip serialization
        assert node.to_dict() == data

    def test_to_markdown(self):
        with open(dir_adf_samples / "node_layout_section.json") as f:
            data = json.load(f)
        node = NodeLayoutSection.from_dict(data)
        md = node.to_markdown().strip()
        assert "Left column" in md
        assert "Right column" in md
        # Columns are separated by blank lines
        assert "\n\n" in md
