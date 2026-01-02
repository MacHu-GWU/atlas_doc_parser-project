# -*- coding: utf-8 -*-

"""
Generate the AI knowledge base for the project.

.. code-block:: bash

    pip install "docpack>=0.1.6,<1.0.0"
"""

import shutil
from pathlib import Path

from atlas_doc_parser.paths import path_enum, PACKAGE_NAME
from docpack.api import GitHubPipeline

dir_here = Path(__file__).absolute().parent
dir_tmp = dir_here / "tmp"
dir_tmp_docs = dir_tmp / "docs"
shutil.rmtree(dir_tmp, ignore_errors=True)
dir_tmp.mkdir()

gh_pipeline = GitHubPipeline(
    domain="github.com",
    account="MacHu-GWU",
    repo=f"{PACKAGE_NAME}-project",
    branch="main",
    dir_repo=path_enum.dir_project_root,
    include=[
        f"{PACKAGE_NAME}/**/*.py",
        "tests/**/*.py",
        "docs/source/**/index.rst",
        "docs/source/**/*.py",
        "bin/**/*.py",
        ".github/workflows/*.yml",
        "README.rst",
        "Makefile",
        "poetry.toml",
        "pyproject.toml",
        ".coveragerc",
        "codecov.yml",
        ".readthedocs.yml",
        "release-history.rst",
    ],
    exclude=[
        f"{PACKAGE_NAME}/tests/**",
        f"{PACKAGE_NAME}/tests/**/*.*",
        f"{PACKAGE_NAME}/vendor/**",
        f"{PACKAGE_NAME}/vendor/**/*.*",
        f"tests/all.py",
        f"tests/**/all.py",
        f"docs/source/index.rst",
        f"docs/source/release-history.rst",
        f"docs/source/conf.py",
        ".venv/**/*.*",
        ".poetry/**/*.*",
        "build/**/*.*",
        "dist/**/*.*",
        "htmlcov/**/*.*",
        "tmp/**/*.*",
        ".pytest_cache/**/*.*",
        ".cache/**/*.*",
        ".coverage",
    ],
    dir_out=dir_tmp_docs,
)
gh_pipeline.fetch()

filename = "all_in_one_knowledge_base.txt"
lines = [
    path.read_text()
    for path in dir_tmp_docs.glob("*.xml")
]
dir_tmp.joinpath(filename).write_text("\n".join(lines), encoding="utf-8")
