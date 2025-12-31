# -*- coding: utf-8 -*-

from pathlib import Path
import requests

dir_here = Path(__file__).absolute().parent
path = dir_here / "adf_json_schema.json"
url = "https://unpkg.com/@atlaskit/adf-schema@51.5.4/dist/json-schema/v1/full.json"
path.write_text(requests.get(url).text, encoding="utf-8")
