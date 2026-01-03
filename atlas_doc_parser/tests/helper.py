# -*- coding: utf-8 -*-

import typing as T
import textwrap
from rich import print as rprint

from ..paths import path_enum
from ..vendor.pytest_cov_helper import (
    run_unit_test as _run_unit_test,
    run_cov_test as _run_cov_test,
)

from ..base import T_BASE
from ..model import T_NODE


def run_unit_test(
    script: str,
):
    _run_unit_test(
        script=script,
        root_dir=f"{path_enum.dir_project_root}",
    )


def run_cov_test(
    script: str,
    module: str,
    preview: bool = False,
    is_folder: bool = False,
):
    _run_cov_test(
        script=script,
        module=module,
        root_dir=f"{path_enum.dir_project_root}",
        htmlcov_dir=f"{path_enum.dir_htmlcov}",
        preview=preview,
        is_folder=is_folder,
    )


# DEFAULT_VERBOSE = True
DEFAULT_VERBOSE = False


def print_adf_json(
    data: T.Any,
    verbose: bool = DEFAULT_VERBOSE,  # True
    # verbose: bool = False,
):
    if verbose:
        print("========== ADF JSON ==========")
        rprint(data)


def check_seder(
    inst: T.Optional[T_BASE],
    verbose: bool = DEFAULT_VERBOSE,  # True
    # verbose: bool = False,
):
    if verbose:
        print("========== Check seder ==========")
    if inst is None:
        return

    if verbose:
        print(f"---------- inst ----------")
        rprint(inst)

    data = inst.to_dict()
    if verbose:
        print(f"---------- data ----------")
        rprint(data)

    inst1 = inst.from_dict(data)
    if verbose:
        print(f"---------- inst1 ----------")
        rprint(inst1)
    assert inst1 == inst

    data1 = inst1.to_dict()
    if verbose:
        print(f"---------- data1 ----------")
        rprint(data1)
    assert inst1.to_dict() == data1


def check_markdown(
    node: T_NODE,
    expected: str,
    verbose: bool = DEFAULT_VERBOSE,  # True
    # verbose: bool = False,
):
    markdown = node.to_markdown().strip()
    expected = textwrap.dedent(expected).strip()
    if verbose:
        print("========== Debug markdown ==========")
        print("nodemd:", [markdown])
        print("expect:", [expected])
        print("---------- nodemd ----------")
        print(markdown)
        print("---------- expect ----------")
        print(expected)
    assert markdown == expected
