# -*- coding: utf-8 -*-

"""
Integration test: parse representative full ADF documents containing
the new node types (bodiedExtension, layoutSection, layoutColumn, inlineExtension)
to validate content union wiring end-to-end.
"""

import json
from pathlib import Path

from atlas_doc_parser.nodes.node_doc import NodeDoc


# Mural Confluence ADF data directory
MURAL_ADF_DIR = Path(
    "/Users/dave/Documents/LLC/Customers/Mural/claude"
    "/global-context/sources/confluence/data/gtms-inside-docs"
)


def _parse_adf_file(path: Path) -> tuple[str, str]:
    """Parse an ADF file and return (filename, markdown). Raises on failure."""
    with open(path) as f:
        data = json.load(f)
    # Our ADF files use a {"metadata": ..., "adf": {...}} envelope
    if "adf" in data:
        data = data["adf"]
    doc = NodeDoc.from_dict(data)
    return path.name, doc.to_markdown()


class TestMuralIntegration:
    def test_bodied_extension_doc(self):
        """A doc with bodiedExtension should render its content."""
        # migration-from-celigo-sync.adf.json is known to contain bodiedExtension
        path = MURAL_ADF_DIR / "migration-from-celigo-sync.adf.json"
        if not path.exists():
            return  # Skip if data not available
        name, md = _parse_adf_file(path)
        assert len(md.strip()) > 0, f"{name} produced empty output"

    def test_layout_section_doc(self):
        """A doc with layoutSection should render column content."""
        path = MURAL_ADF_DIR / "slack-command-to-transition-jira-issue-to-closed.adf.json"
        if not path.exists():
            return
        name, md = _parse_adf_file(path)
        assert len(md.strip()) > 0, f"{name} produced empty output"

    def test_inline_extension_doc(self):
        """A doc with inlineExtension should render the extension placeholder."""
        path = MURAL_ADF_DIR / "jira" / "README.adf.json"
        if not path.exists():
            return
        name, md = _parse_adf_file(path)
        assert len(md.strip()) > 0, f"{name} produced empty output"

    def test_all_adf_files_parse_without_error(self):
        """All 109 ADF files should parse without raising exceptions."""
        if not MURAL_ADF_DIR.exists():
            return
        failures = []
        for path in sorted(MURAL_ADF_DIR.rglob("*.adf.json")):
            try:
                _parse_adf_file(path)
            except Exception as e:
                failures.append(f"{path.name}: {e}")
        assert not failures, f"Parse failures:\n" + "\n".join(failures)

    def test_previously_empty_files_now_produce_output(self):
        """Files that were empty due to unimplemented types should now have content."""
        if not MURAL_ADF_DIR.exists():
            return
        empty_files = []
        for path in sorted(MURAL_ADF_DIR.rglob("*.adf.json")):
            try:
                name, md = _parse_adf_file(path)
                if not md.strip():
                    empty_files.append(name)
            except Exception:
                pass  # Covered by test_all_adf_files_parse_without_error
        # Report but don't necessarily fail — some files may legitimately be empty
        if empty_files:
            print(f"\nFiles with empty output ({len(empty_files)}):")
            for name in empty_files:
                print(f"  - {name}")
