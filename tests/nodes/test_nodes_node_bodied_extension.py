# -*- coding: utf-8 -*-

import json
from pathlib import Path

from atlas_doc_parser.nodes.node_bodied_extension import NodeBodiedExtension


dir_adf_samples = Path(__file__).parent.parent / "adf_samples"


class TestNodeBodiedExtension:
    def test_from_dict_and_seder(self):
        with open(dir_adf_samples / "node_bodied_extension.json") as f:
            data = json.load(f)
        node = NodeBodiedExtension.from_dict(data)
        assert node.type == "bodiedExtension"
        assert node.attrs.extensionKey == "excerpt"
        assert node.attrs.extensionType == "com.atlassian.confluence.macro.core"
        # Roundtrip serialization
        assert node.to_dict() == data

    def test_to_markdown(self):
        with open(dir_adf_samples / "node_bodied_extension.json") as f:
            data = json.load(f)
        node = NodeBodiedExtension.from_dict(data)
        md = node.to_markdown().strip()
        assert md == "This is excerpt content."

    def test_with_table_content(self):
        """Test bodiedExtension containing a table (Page Properties macro)."""
        with open(dir_adf_samples / "node_doc_with_unimplemented_model.json") as f:
            data = json.load(f)
        # Extract the bodiedExtension node from the doc
        be_data = data["content"][0]
        node = NodeBodiedExtension.from_dict(be_data)
        md = node.to_markdown()
        assert "owner" in md
        assert "alice" in md
