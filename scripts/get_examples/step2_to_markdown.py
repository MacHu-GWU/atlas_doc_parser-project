# -*- coding: utf-8 -*-

"""
This script is used to convert Atlassian Document Format to Markdown.
"""

from atlas_doc_parser.model import NodeDoc
import json
from pathlib import Path
from rich import print as rprint

dir_here = Path(__file__).absolute().parent

path = dir_here.joinpath("tmp", "Atlassian Document Format Parser Test.json")
# path = dir_here.joinpath("tmp", "Welcome to BunnymanTech LLC: Our Story and Mission.json")

data = json.loads(path.read_text())
node_doc = NodeDoc.from_dict(data, ignore_error=True)

path_md = dir_here.joinpath("export_as_markdown.md")
text = node_doc.to_markdown()
path_md.write_text(text)
