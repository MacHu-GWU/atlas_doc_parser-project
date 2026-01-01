# -*- coding: utf-8 -*-

"""
ADF Code Generator

This script generates Python dataclass code for ADF nodes and marks
based on the JSON Schema.

Generated files:
- nodes/*.py: Auto-generated, ALWAYS overwritten on each run
- nodes/parse.py: Auto-generated registry, ALWAYS overwritten on each run
- mixins/*.py: Stub files only created for NEW types, NEVER overwritten
              (mixins are manually maintained after initial creation)
"""

import json
import re
from pathlib import Path
from jinja2 import Template


# =============================================================================
# Paths
# =============================================================================
dir_here = Path(__file__).parent
dir_project = dir_here.parent.parent
dir_templates = dir_here / "templates"
path_schema = dir_here / "adf_json_schema.json"
dir_nodes = dir_project / "atlas_doc_parser" / "nodes"
dir_mixins = dir_project / "atlas_doc_parser" / "mixins"


# =============================================================================
# Load Templates
# =============================================================================
def load_template(name: str) -> Template:
    """Load a Jinja2 template from the templates directory."""
    path = dir_templates / name
    with open(path) as f:
        return Template(f.read())


tpl_mark = load_template("mark.py.jinja2")
tpl_node = load_template("node.py.jinja2")
tpl_parse = load_template("parse.py.jinja2")
tpl_mixin_mark = load_template("mixin_mark.py.jinja2")
tpl_mixin_node = load_template("mixin_node.py.jinja2")


# =============================================================================
# Helper functions
# =============================================================================
def to_class_name(type_name: str, prefix: str) -> str:
    """Convert type name to class name (e.g., 'strong' -> 'MarkStrong')."""
    class_part = type_name[0].upper() + type_name[1:]
    return f"{prefix}{class_part}"


def to_module_name(type_name: str, prefix: str) -> str:
    """Convert type name to module name (e.g., 'strong' -> 'mark_strong')."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', type_name)
    snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return f"{prefix.lower()}_{snake}"


def extract_schema_info(schema: dict, def_name: str) -> dict:
    """Extract information from a schema definition."""
    definition = schema["definitions"].get(def_name, {})
    info = {
        "has_attrs": False,
        "has_content": False,
        "has_marks": False,
        "attrs_fields": [],
        "extra_fields": [],
    }

    props = definition.get("properties", {})

    # Handle allOf
    if "allOf" in definition:
        for item in definition["allOf"]:
            if "properties" in item:
                props.update(item["properties"])

    # Check for attrs
    if "attrs" in props:
        info["has_attrs"] = True
        attrs_def = props["attrs"]
        if "properties" in attrs_def:
            for field_name, field_def in attrs_def["properties"].items():
                field_type = schema_type_to_python(field_def)
                info["attrs_fields"].append({
                    "name": field_name,
                    "type": field_type,
                    "default": "OPT",
                })

    # Check for content
    if "content" in props:
        info["has_content"] = True

    # Check for marks
    if "marks" in props:
        info["has_marks"] = True

    # Check for text field (for text node)
    if "text" in props:
        info["extra_fields"].append({
            "name": "text",
            "type": "str",
            "default": "OPT",
        })

    # Check for version field (for doc node)
    if "version" in props:
        info["extra_fields"].append({
            "name": "version",
            "type": "int",
            "default": "dataclasses.field(default=1)",
        })

    return info


def schema_type_to_python(prop_schema: dict) -> str:
    """Convert JSON Schema type to Python type hint."""
    if "enum" in prop_schema:
        return "str"
    if "type" in prop_schema:
        type_map = {
            "string": "str",
            "integer": "int",
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict[str, T.Any]",
        }
        return type_map.get(prop_schema["type"], "T.Any")
    return "T.Any"


def main():
    # Load schema
    with open(path_schema) as f:
        schema = json.load(f)

    # Separate mark and node definitions
    mark_defs = {}
    node_defs = {}

    for def_name, definition in schema["definitions"].items():
        if def_name.endswith("_mark"):
            props = definition.get("properties", {})
            type_prop = props.get("type", {})
            if "enum" in type_prop:
                type_name = type_prop["enum"][0]
                mark_defs[type_name] = def_name
        elif def_name.endswith("_node"):
            props = definition.get("properties", {})
            if "allOf" in definition:
                for item in definition["allOf"]:
                    if "properties" in item:
                        props.update(item["properties"])
            type_prop = props.get("type", {})
            if "enum" in type_prop:
                type_name = type_prop["enum"][0]
                # Skip variants like paragraph_with_alignment_node
                if "_with_" not in def_name:
                    node_defs[type_name] = def_name

    print(f"Mark definitions: {len(mark_defs)}")
    print(f"Node definitions: {len(node_defs)}")

    # Generate mark files
    marks_info = []
    for type_name, def_name in sorted(mark_defs.items()):
        class_name = to_class_name(type_name, "Mark")
        module_name = to_module_name(type_name, "mark")
        type_enum = type_name
        schema_info = extract_schema_info(schema, def_name)

        content = tpl_mark.render(
            type_name=type_name,
            type_enum=type_enum,
            class_name=class_name,
            module_name=module_name,
            has_mixin=True,  # Always include mixin import
            has_attrs=schema_info["has_attrs"],
            attrs_fields=schema_info["attrs_fields"],
        )

        path_output = dir_nodes / f"{module_name}.py"
        with open(path_output, "w") as f:
            f.write(content)
        print(f"Generated: {path_output.name}")

        marks_info.append({
            "type_name": type_name,
            "class_name": class_name,
            "module_name": module_name,
        })

    # Generate node files
    nodes_info = []
    for type_name, def_name in sorted(node_defs.items()):
        class_name = to_class_name(type_name, "Node")
        module_name = to_module_name(type_name, "node")
        type_enum = type_name
        schema_info = extract_schema_info(schema, def_name)

        content = tpl_node.render(
            type_name=type_name,
            type_enum=type_enum,
            class_name=class_name,
            module_name=module_name,
            has_mixin=True,  # Always include mixin import
            has_attrs=schema_info["has_attrs"],
            has_content=schema_info["has_content"],
            has_marks=schema_info["has_marks"],
            attrs_fields=schema_info["attrs_fields"],
            extra_fields=schema_info["extra_fields"],
        )

        path_output = dir_nodes / f"{module_name}.py"
        with open(path_output, "w") as f:
            f.write(content)
        print(f"Generated: {path_output.name}")

        nodes_info.append({
            "type_name": type_name,
            "class_name": class_name,
            "module_name": module_name,
        })

    # Generate parse.py
    parse_content = tpl_parse.render(
        marks=marks_info,
        nodes=nodes_info,
    )

    path_parse = dir_nodes / "parse.py"
    with open(path_parse, "w") as f:
        f.write(parse_content)
    print(f"Generated: {path_parse.name}")

    # Generate stub mixin files
    # IMPORTANT: Mixin files are NEVER overwritten - they are manually maintained.
    # Only create stub files for NEW types that don't have a mixin yet.
    mixin_created = 0
    mixin_skipped = 0

    for info in marks_info:
        path_mixin = dir_mixins / f"{info['module_name']}.py"
        if path_mixin.exists():
            mixin_skipped += 1
        else:
            mixin_content = tpl_mixin_mark.render(
                type_name=info["type_name"],
                class_name=info["class_name"],
                module_name=info["module_name"],
            )
            with open(path_mixin, "w") as f:
                f.write(mixin_content)
            print(f"Created mixin stub: {path_mixin.name}")
            mixin_created += 1

    for info in nodes_info:
        path_mixin = dir_mixins / f"{info['module_name']}.py"
        if path_mixin.exists():
            mixin_skipped += 1
        else:
            mixin_content = tpl_mixin_node.render(
                type_name=info["type_name"],
                class_name=info["class_name"],
                module_name=info["module_name"],
            )
            with open(path_mixin, "w") as f:
                f.write(mixin_content)
            print(f"Created mixin stub: {path_mixin.name}")
            mixin_created += 1

    print(f"\nDone! Generated {len(marks_info)} marks, {len(nodes_info)} nodes, and parse.py")
    print(f"Mixins: {mixin_skipped} existing (preserved), {mixin_created} new stubs created")


if __name__ == "__main__":
    main()
