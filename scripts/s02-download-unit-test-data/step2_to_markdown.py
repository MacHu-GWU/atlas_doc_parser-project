# -*- coding: utf-8 -*-

"""
This script is used to convert Atlassian Document Format to Markdown.
"""

from atlas_doc_parser.model import NodeDoc
import json
from pathlib import Path
from rich import print as rprint

dir_here = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")

for path in dir_tmp.glob("*.json"):
    data = json.loads(path.read_text())
    node_doc = NodeDoc.from_dict(data, ignore_error=True)

    path_md = dir_tmp.joinpath(path.stem + ".md")
    print(f"{path.name} -> {path_md.name}")
    text = node_doc.to_markdown()
    path_md.write_text(text)
