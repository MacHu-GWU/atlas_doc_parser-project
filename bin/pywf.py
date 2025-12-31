# -*- coding: utf-8 -*-

"""
Initialize PyWf object from a ``pyproject.toml`` file.
"""

from pathlib import Path
from pywf_open_source.api import PyWf

dir_here = Path(__file__).absolute().parent
path_pyproject_toml = dir_here.parent.joinpath("pyproject.toml")
pywf = PyWf.from_pyproject_toml(path_pyproject_toml)
