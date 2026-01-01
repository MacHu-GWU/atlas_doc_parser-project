# -*- coding: utf-8 -*-

"""
This script is used to extract Atlassian Document Format content from Confluence.
"""

import json
import time
import shutil
from pathlib import Path
from pyatlassian.api import confluence

dir_here = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")

dir_home = Path.home()
path = dir_home.joinpath(".atlassian", "sanhehu", "sanhe-dev.txt")
api_token = path.read_text().strip()
conf = confluence.Confluence(
    url="https://sanhehu.atlassian.net",
    username="husanhe@gmail.com",
    password=api_token,
)


def get_page_by_id(page_id: int) -> tuple[str, dict]:
    """
    Get page title and body (atlas_doc_format) by page_id.
    """
    res = conf.get_page_by_id(
        page_id=page_id,
        body_format="atlas_doc_format",
        include_labels=True,
        include_properties=True,
        include_operations=True,
        include_likes=True,
        include_versions=True,
        include_version=True,
        include_favorited_by_current_user_status=True,
    )
    title = res["title"]
    body = res["body"]["atlas_doc_format"]["value"]
    body_data = json.loads(body)
    return title, body_data


def main(page_id_list: list[int]):
    """
    Convert page content to json file and save to disk.
    """
    if dir_tmp.exists():
        shutil.rmtree(dir_tmp)
    dir_tmp.mkdir()
    for page_id in page_id_list:
        title, body_data = get_page_by_id(page_id)
        path = dir_tmp.joinpath(f"{title}.json")
        path.write_text(json.dumps(body_data, ensure_ascii=False, indent=2))
        time.sleep(1)


if __name__ == "__main__":
    id_list = [
        294223873,  # page_id = '294223873', page_title = 'Atlassian Document Format Parser Test', page_url = 'https://sanhehu.atlassian.net/wiki/spaces/JWBMT/pages/294223873/Atlassian+Document+Format+Parser+Test'
        # 293077005,  # page_id = '293077005', page_title = 'Welcome to BunnymanTech LLC: Our Story and Mission', page_url = 'https://sanhehu.atlassian.net/wiki/spaces/JWBMT/pages/293077005/Welcome+to+BunnymanTech+LLC+Our+Story+and+Mission'
    ]
    main(id_list)
