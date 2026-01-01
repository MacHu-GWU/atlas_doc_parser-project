# -*- coding: utf-8 -*-

from home_secret_toml.api import hs
from sanhe_confluence_sdk.client import Confluence

client = Confluence(
    url=hs.v("atlassian.accounts.sh.site_url"),
    username=hs.v("atlassian.accounts.sh.users.sh.email"),
    password=hs.v("atlassian.accounts.sh.users.sh.secrets.sync_page.value"),
)
