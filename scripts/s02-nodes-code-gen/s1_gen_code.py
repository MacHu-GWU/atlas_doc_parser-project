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

Usage:
    .venv/bin/python scripts/s01-adf-json-schema-analysis/s3_gen_code.py
"""

import re
import typing as T
from pathlib import Path
from dataclasses import dataclass

from jinja2 import Environment, FileSystemLoader

from atlas_doc_parser.tests.data.schema import adf_json_schema


# =============================================================================
# Paths
# =============================================================================
dir_here = Path(__file__).parent
dir_project = dir_here.parent.parent
dir_templates = dir_here / "templates"
dir_nodes = dir_project / "atlas_doc_parser" / "nodes"
dir_mixins = dir_project / "atlas_doc_parser" / "mixins"


# =============================================================================
# Load Templates
# =============================================================================
env = Environment(loader=FileSystemLoader(dir_templates), trim_blocks=True)
tpl_mark = env.get_template("mark.py.jinja2")
tpl_node = env.get_template("node.py.jinja2")
tpl_parse = env.get_template("parse.py.jinja2")
tpl_mixin_mark = env.get_template("mixin_mark.py.jinja2")
tpl_mixin_node = env.get_template("mixin_node.py.jinja2")


# =============================================================================
# Data Classes for Schema Info
# =============================================================================
@dataclass
class FieldInfo:
    """Information about a field in a schema definition."""

    name: str
    type: str
    default: str
    required: bool = False


@dataclass
class DefinitionNames:
    """
    Name mappings for a schema definition.

    Contains the original definition name and derived Python naming conventions:

    - module_name: snake_case module name (e.g., 'mark_strong', 'node_paragraph')
    - class_name: PascalCase class name (e.g., 'MarkStrong', 'NodeParagraph')
    - attrs_class_name: PascalCase attrs class name (e.g., 'MarkStrongAttrs')
    - mixin_class_name: PascalCase mixin class name (e.g., 'MarkStrongMixin')
    - type_name: Derived type name for docs (e.g., 'table_cell', 'paragraph')
    - type_enum: The actual ADF type enum value from schema (e.g., 'tableCell', 'paragraph')
    """

    def_name: str
    module_name: str
    class_name: str
    attrs_class_name: str
    mixin_class_name: str
    type_name: str
    type_enum: str


@dataclass
class SchemaInfo:
    """
    Extracted schema information for a definition.

    Contains structured data about the definition's properties:
    - attrs_fields: Fields within the 'attrs' property
    - extra_fields: Non-standard fields like 'text', 'version'
    - has_attrs: Whether the definition has an 'attrs' property
    - has_content: Whether the definition has a 'content' property
    - has_marks: Whether the definition has a 'marks' property
    - attrs_required: List of required field names in attrs
    """

    attrs_fields: list[FieldInfo]
    extra_fields: list[FieldInfo]
    has_attrs: bool
    has_content: bool
    has_marks: bool
    attrs_required: list[str]


# =============================================================================
# Name Mapping Utility
# =============================================================================
def get_type_enum_from_schema(def_name: str) -> str:
    """
    Extract the actual type enum value from the schema definition.

    The ADF schema defines the type enum in properties.type.enum[0].
    For example, 'table_cell_node' has type enum value 'tableCell'.

    Args:
        def_name: The definition name (e.g., 'table_cell_node')

    Returns:
        The type enum value from the schema (e.g., 'tableCell')
    """
    definition = adf_json_schema.data["definitions"].get(def_name, {})
    props = definition.get("properties", {})

    # Handle allOf - merge properties from all schemas
    if "allOf" in definition:
        for item in definition["allOf"]:
            if "properties" in item:
                props.update(item["properties"])

    type_prop = props.get("type", {})
    if "enum" in type_prop and type_prop["enum"]:
        return type_prop["enum"][0]

    # Fallback: derive from definition name
    if def_name.endswith("_mark"):
        return def_name[:-5]
    elif def_name.endswith("_node"):
        return def_name[:-5]
    return def_name


def camel_to_snake(name: str) -> str:
    """
    Convert camelCase or PascalCase to snake_case.

    Examples:
        'bulletList' -> 'bullet_list'
        'backgroundColor' -> 'background_color'
        'code_inline' -> 'code_inline' (already snake_case)
    """
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_pascal(name: str) -> str:
    """
    Convert snake_case to PascalCase.

    Examples:
        'bullet_list' -> 'BulletList'
        'code_inline' -> 'CodeInline'
        'table_cell' -> 'TableCell'
    """
    return "".join(word.capitalize() for word in name.split("_"))


def def_name_to_names(def_name: str) -> DefinitionNames:
    """
    Convert a definition name to Python naming conventions.

    Handles naming patterns:

    - 'bulletList_node' → module: 'node_bullet_list', class: 'NodeBulletList'
    - 'strong_mark' → module: 'mark_strong', class: 'MarkStrong'
    - 'backgroundColor_mark' → module: 'mark_background_color', class: 'MarkBackgroundColor'
    - 'table_cell_node' → module: 'node_table_cell', class: 'NodeTableCell'
    - 'code_inline_node' → module: 'node_code_inline', class: 'NodeCodeInline'

    Args:
        def_name: The JSON schema definition name (e.g., 'bulletList_node')

    Returns:
        DefinitionNames with all derived names
    """
    # Determine if it's a mark or node and extract the base type name
    if def_name.endswith("_mark"):
        prefix = "mark"
        type_name = def_name[:-5]  # Remove '_mark'
    elif def_name.endswith("_node"):
        prefix = "node"
        type_name = def_name[:-5]  # Remove '_node'
    else:
        raise ValueError(f"Unknown definition type: {def_name}")

    # Get the actual type enum value from the schema
    type_enum = get_type_enum_from_schema(def_name)

    # Convert type name to snake_case for module name
    # Handles both camelCase (bulletList) and existing snake_case (table_cell)
    snake_name = camel_to_snake(type_name)

    # Build module name: prefix_snake_name (e.g., 'node_bullet_list')
    module_name = f"{prefix}_{snake_name}"

    # Build class name: PascalCase prefix + PascalCase type
    # e.g., 'Node' + 'BulletList' = 'NodeBulletList'
    # For snake_case types like 'table_cell', convert to 'TableCell'
    prefix_pascal = prefix.capitalize()
    type_pascal = snake_to_pascal(snake_name)
    class_name = f"{prefix_pascal}{type_pascal}"

    return DefinitionNames(
        def_name=def_name,
        module_name=module_name,
        class_name=class_name,
        attrs_class_name=f"{class_name}Attrs",
        mixin_class_name=f"{class_name}Mixin",
        type_name=type_name,
        type_enum=type_enum,
    )


def get_all_definitions() -> tuple[list[str], list[str]]:
    """
    Get all mark and node definition names from the schema.

    Filters out variant definitions (e.g., 'paragraph_with_alignment_node')
    and returns only base definitions.

    Returns:
        Tuple of (mark_def_names, node_def_names)
    """
    mark_defs = []
    node_defs = []

    for def_name in adf_json_schema.data["definitions"]:
        # Skip variant definitions
        if "_with_" in def_name:
            continue
        if def_name.endswith("_root_only_node"):
            continue
        if def_name.endswith("_full_node"):
            continue
        # Skip abstract/content definitions
        if def_name.endswith("_content"):
            continue
        if def_name == "inline_node":
            continue
        if def_name == "non_nestable_block_content":
            continue
        if def_name == "block_content":
            continue
        # Skip definitions that inherit from other nodes without their own type
        # These are schema-level specializations, not actual ADF types
        if def_name in (
            "code_inline_node",
            "formatted_text_inline_node",
            "mediaSingle_caption_node",
        ):
            continue

        if def_name.endswith("_mark"):
            mark_defs.append(def_name)
        elif def_name.endswith("_node"):
            node_defs.append(def_name)

    return sorted(mark_defs), sorted(node_defs)


# =============================================================================
# Schema Type Conversion
# =============================================================================
def schema_type_to_python(prop_schema: dict, required: bool = False) -> str:
    """
    Convert JSON Schema type to Python type hint.

    Args:
        prop_schema: The JSON Schema property definition
        required: Whether the field is required

    Returns:
        Python type hint string
    """
    if "enum" in prop_schema:
        return "str"
    if "$ref" in prop_schema:
        # References to other definitions - use T.Any for now
        return "T.Any"
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
    if "anyOf" in prop_schema or "oneOf" in prop_schema:
        return "T.Any"
    return "T.Any"


def get_field_default(required: bool) -> str:
    """
    Get the default value expression for a field.

    Args:
        required: Whether the field is required

    Returns:
        'OPT' for optional fields, empty string for required fields
    """
    return "" if required else "OPT"


# =============================================================================
# Schema Extraction
# =============================================================================
def extract_schema_info(def_name: str) -> SchemaInfo:
    """
    Extract structured information from a schema definition.

    Handles:
    - Simple object definitions with direct properties
    - allOf definitions that merge multiple schemas
    - Required vs optional field detection
    - Special fields like 'text', 'version'

    Args:
        def_name: The definition name to extract info from

    Returns:
        SchemaInfo with all extracted information
    """
    definition = adf_json_schema.data["definitions"].get(def_name, {})

    info = SchemaInfo(
        attrs_fields=[],
        extra_fields=[],
        has_attrs=False,
        has_content=False,
        has_marks=False,
        attrs_required=[],
    )

    props = definition.get("properties", {})
    top_required = definition.get("required", [])

    # Handle allOf - merge properties from all schemas
    if "allOf" in definition:
        for item in definition["allOf"]:
            if "properties" in item:
                props.update(item["properties"])
            if "required" in item:
                top_required.extend(item["required"])

    # Check for attrs
    if "attrs" in props:
        info.has_attrs = True
        attrs_def = props["attrs"]
        attrs_required = attrs_def.get("required", [])
        info.attrs_required = attrs_required

        if "properties" in attrs_def:
            for field_name, field_def in attrs_def["properties"].items():
                is_required = field_name in attrs_required
                field_type = schema_type_to_python(field_def, is_required)
                info.attrs_fields.append(
                    FieldInfo(
                        name=field_name,
                        type=field_type,
                        default=get_field_default(is_required),
                        required=is_required,
                    )
                )

        # Sort fields: required fields first (no default), then optional
        info.attrs_fields.sort(key=lambda f: (not f.required, f.name))

    # Check for content
    if "content" in props:
        info.has_content = True

    # Check for marks
    if "marks" in props:
        info.has_marks = True

    # Check for special fields
    if "text" in props:
        info.extra_fields.append(
            FieldInfo(
                name="text",
                type="str",
                default="OPT",
                required=False,
            )
        )

    if "version" in props:
        info.extra_fields.append(
            FieldInfo(
                name="version",
                type="int",
                default="dataclasses.field(default=1)",
                required=False,
            )
        )

    return info


# =============================================================================
# Code Generation
# =============================================================================
def generate_mark_file(names: DefinitionNames, schema_info: SchemaInfo) -> str:
    """Generate Python code for a mark dataclass."""
    return tpl_mark.render(
        type_name=names.type_name,
        type_enum=names.type_enum,
        class_name=names.class_name,
        module_name=names.module_name,
        has_mixin=True,
        has_attrs=schema_info.has_attrs,
        attrs_fields=[
            {
                "name": f.name,
                "type": f.type,
                "default": f.default,
                "required": f.required,
            }
            for f in schema_info.attrs_fields
        ],
    )


def generate_node_file(names: DefinitionNames, schema_info: SchemaInfo) -> str:
    """Generate Python code for a node dataclass."""
    return tpl_node.render(
        type_name=names.type_name,
        type_enum=names.type_enum,
        class_name=names.class_name,
        module_name=names.module_name,
        has_mixin=True,
        has_attrs=schema_info.has_attrs,
        has_content=schema_info.has_content,
        has_marks=schema_info.has_marks,
        attrs_fields=[
            {
                "name": f.name,
                "type": f.type,
                "default": f.default,
                "required": f.required,
            }
            for f in schema_info.attrs_fields
        ],
        extra_fields=[
            {
                "name": f.name,
                "type": f.type,
                "default": f.default,
            }
            for f in schema_info.extra_fields
        ],
    )


def generate_parse_file(
    marks_info: list[dict],
    nodes_info: list[dict],
) -> str:
    """Generate Python code for the parse.py registry."""
    return tpl_parse.render(
        marks=marks_info,
        nodes=nodes_info,
    )


def generate_mixin_stub(names: DefinitionNames, is_mark: bool) -> str:
    """Generate a stub mixin file for a new type."""
    tpl = tpl_mixin_mark if is_mark else tpl_mixin_node
    return tpl.render(
        type_name=names.type_name,
        class_name=names.class_name,
        module_name=names.module_name,
    )


# =============================================================================
# Main
# =============================================================================
def main():
    """
    Main entry point for code generation.

    Steps:
    1. Query all definitions from the schema
    2. Generate mark files
    3. Generate node files
    4. Generate parse.py registry
    5. Create stub mixin files for new types (never overwrites existing)
    """
    # Get all definitions
    mark_defs, node_defs = get_all_definitions()
    print(f"Found {len(mark_defs)} mark definitions")
    print(f"Found {len(node_defs)} node definitions")

    # Generate mark files
    marks_info = []
    for def_name in mark_defs:
        names = def_name_to_names(def_name)
        schema_info = extract_schema_info(def_name)

        content = generate_mark_file(names, schema_info)
        path_output = dir_nodes / f"{names.module_name}.py"
        with open(path_output, "w") as f:
            f.write(content)
        print(f"Generated: {path_output.name}")

        marks_info.append(
            {
                "type_name": names.type_name,
                "type_enum": names.type_enum,
                "class_name": names.class_name,
                "module_name": names.module_name,
            }
        )

    # Generate node files
    nodes_info = []
    for def_name in node_defs:
        names = def_name_to_names(def_name)
        schema_info = extract_schema_info(def_name)

        content = generate_node_file(names, schema_info)
        path_output = dir_nodes / f"{names.module_name}.py"
        with open(path_output, "w") as f:
            f.write(content)
        print(f"Generated: {path_output.name}")

        nodes_info.append(
            {
                "type_name": names.type_name,
                "type_enum": names.type_enum,
                "class_name": names.class_name,
                "module_name": names.module_name,
            }
        )

    # Generate parse.py
    parse_content = generate_parse_file(marks_info, nodes_info)
    path_parse = dir_nodes / "parse.py"
    with open(path_parse, "w") as f:
        f.write(parse_content)
    print(f"Generated: {path_parse.name}")

    # Generate stub mixin files (only for NEW types)
    mixin_created = 0
    mixin_skipped = 0

    for info in marks_info:
        path_mixin = dir_mixins / f"{info['module_name']}.py"
        if path_mixin.exists():
            mixin_skipped += 1
        else:
            names = def_name_to_names(f"{info['type_name']}_mark")
            mixin_content = generate_mixin_stub(names, is_mark=True)
            with open(path_mixin, "w") as f:
                f.write(mixin_content)
            print(f"Created mixin stub: {path_mixin.name}")
            mixin_created += 1

    for info in nodes_info:
        path_mixin = dir_mixins / f"{info['module_name']}.py"
        if path_mixin.exists():
            mixin_skipped += 1
        else:
            names = def_name_to_names(f"{info['type_name']}_node")
            mixin_content = generate_mixin_stub(names, is_mark=False)
            with open(path_mixin, "w") as f:
                f.write(mixin_content)
            print(f"Created mixin stub: {path_mixin.name}")
            mixin_created += 1

    print(f"\nDone!")
    print(f"Generated {len(marks_info)} marks, {len(nodes_info)} nodes, and parse.py")
    print(
        f"Mixins: {mixin_skipped} existing (preserved), {mixin_created} new stubs created"
    )


if __name__ == "__main__":
    main()
