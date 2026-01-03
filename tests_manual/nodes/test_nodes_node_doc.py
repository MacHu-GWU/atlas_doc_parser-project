# -*- coding: utf-8 -*-

from atlas_doc_parser.nodes.node_doc import NodeDoc
from atlas_doc_parser.paths import path_enum
from atlas_doc_parser.tests.data.samples import AdfSampleEnum


class TestNodeDoc:
    def test_node_doc_basic(self):
        data = AdfSampleEnum.node_doc.page.adf_no_cache
        node = NodeDoc.from_dict(data)
        md = node.to_markdown()
        path = path_enum.dir_project_root / "tmp" / "test_node_doc_basic.md"
        path.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    from atlas_doc_parser.tests import run_unit_test

    run_unit_test(__file__)
