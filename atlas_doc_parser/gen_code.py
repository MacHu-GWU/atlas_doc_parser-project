# -*- coding: utf-8 -*-

"""
Code generation utilities for atlas_doc_parser.

This module provides utilities to auto-generate the api.py file by scanning
the marks/ and nodes/ directories for public API classes.
"""

import dataclasses
import importlib
import inspect
from pathlib import Path

from jinja2 import Template

from .paths import path_enum


@dataclasses.dataclass
class PublicAPI:
    """
    Metadata for a public API class.

    :param module_name: The module name (e.g., "mark_link", "node_heading")
    :param class_name: The class name (e.g., "MarkLink", "NodeHeading")
    :param is_attrs: Whether this is an Attrs class (e.g., "MarkLinkAttrs")
    :param is_type_alias: Whether this is a type alias (e.g., ``T_NODE_...``)
    """

    module_name: str
    class_name: str
    is_attrs: bool = False
    is_type_alias: bool = False

    @property
    def relative_import_path(self) -> str:
        """
        Get the relative import path for this API.

        For marks: .marks.mark_xxx
        For nodes: .nodes.node_xxx
        """
        if self.module_name.startswith("mark_"):
            return f".marks.{self.module_name}"
        elif self.module_name.startswith("node_"):
            return f".nodes.{self.module_name}"
        else:
            raise ValueError(f"Unknown module type: {self.module_name}")


def scan_module_for_public_apis(
    module_path: Path,
    base_classes: tuple,
) -> list[PublicAPI]:
    """
    Scan a module for public API classes.

    :param module_path: Path to the Python module file
    :param base_classes: Tuple of base classes to check inheritance against

    :return: List of PublicAPI objects for classes that inherit from base_classes
    """
    module_name = module_path.stem  # e.g., "mark_link"

    # Determine the full module path for import
    if "marks" in module_path.parts:
        full_module_name = f"atlas_doc_parser.marks.{module_name}"
    elif "nodes" in module_path.parts:
        full_module_name = f"atlas_doc_parser.nodes.{module_name}"
    else:
        return []

    # Import the module
    try:
        module = importlib.import_module(full_module_name)
    except ImportError as e:
        print(f"Warning: Could not import {full_module_name}: {e}")
        return []

    public_apis = []

    # Get all public members of the module
    for name, obj in inspect.getmembers(module):
        # Skip private/protected members
        if name.startswith("_"):
            continue

        # Check if it's a class defined in this module
        if inspect.isclass(obj) and obj.__module__ == full_module_name:
            # Check if it inherits from any of the base classes
            if issubclass(obj, base_classes):
                is_attrs = name.endswith("Attrs")
                public_apis.append(
                    PublicAPI(
                        module_name=module_name,
                        class_name=name,
                        is_attrs=is_attrs,
                    )
                )

        # Check for type aliases (T_NODE_*, T_MARK_*)
        # Type aliases are typically typing constructs
        if name.startswith("T_NODE_") or name.startswith("T_MARK_"):
            public_apis.append(
                PublicAPI(
                    module_name=module_name,
                    class_name=name,
                    is_type_alias=True,
                )
            )

    return public_apis


def scan_all_modules() -> dict[str, list[PublicAPI]]:
    """
    Scan all mark and node modules for public APIs.

    :return: Dictionary with keys 'marks' and 'nodes', each containing a list of PublicAPI
    """
    # Import base classes
    from .mark_or_node import Base

    base_classes = (Base,)

    result = {
        "marks": [],
        "nodes": [],
    }

    # Scan marks directory
    marks_dir = path_enum.dir_package / "marks"
    for module_path in sorted(marks_dir.glob("mark_*.py")):
        apis = scan_module_for_public_apis(module_path, base_classes)
        result["marks"].extend(apis)

    # Scan nodes directory
    nodes_dir = path_enum.dir_package / "nodes"
    for module_path in sorted(nodes_dir.glob("node_*.py")):
        apis = scan_module_for_public_apis(module_path, base_classes)
        result["nodes"].extend(apis)

    return result


def generate_api_py() -> str:
    """
    Generate the content for api.py using Jinja2 template.

    :return: The generated Python source code
    """
    # Load the template
    template_path = path_enum.dir_package / "templates" / "api.py.jinja"
    with open(template_path, "r") as f:
        template_content = f.read()

    template = Template(template_content)

    # Scan for all public APIs
    all_apis = scan_all_modules()

    # Group APIs by module for cleaner output
    marks_by_module: dict[str, list[PublicAPI]] = {}
    for api in all_apis["marks"]:
        if api.module_name not in marks_by_module:
            marks_by_module[api.module_name] = []
        marks_by_module[api.module_name].append(api)

    nodes_by_module: dict[str, list[PublicAPI]] = {}
    for api in all_apis["nodes"]:
        if api.module_name not in nodes_by_module:
            nodes_by_module[api.module_name] = []
        nodes_by_module[api.module_name].append(api)

    # Render the template
    content = template.render(
        marks_by_module=marks_by_module,
        nodes_by_module=nodes_by_module,
    )

    return content


def main():
    """
    Main entry point for code generation.

    Generates the api.py file by scanning marks/ and nodes/ directories.
    """
    content = generate_api_py()

    # Write the generated content to api.py
    api_py_path = path_enum.dir_package / "api.py"
    with open(api_py_path, "w") as f:
        f.write(content)

    print(f"Generated {api_py_path}")


if __name__ == "__main__":
    main()
