# -*- coding: utf-8 -*-

"""
Analyze ADF JSON Schema dependencies and generate markdown report.

This script:
1. Parses the ADF JSON Schema
2. Extracts all node and mark definitions
3. Builds a dependency graph based on $ref references
4. Performs topological sort to determine implementation order
5. Outputs a markdown file
"""

import json
from pathlib import Path
from collections import defaultdict


def extract_refs(obj: dict | list | str, refs: set) -> None:
    """Recursively extract all $ref references from a schema object."""
    if isinstance(obj, dict):
        if "$ref" in obj:
            ref = obj["$ref"]
            if ref.startswith("#/definitions/"):
                def_name = ref[len("#/definitions/"):]
                refs.add(def_name)
        for value in obj.values():
            extract_refs(value, refs)
    elif isinstance(obj, list):
        for item in obj:
            extract_refs(item, refs)


def get_base_type(def_name: str) -> str | None:
    """Extract base type from definition name."""
    if def_name.endswith("_node"):
        name = def_name[:-5]
        if "_with_" in name:
            name = name.split("_with_")[0]
        return name
    elif def_name.endswith("_mark"):
        return def_name[:-5]
    return None


def topological_sort(graph: dict[str, set[str]]) -> list[str]:
    """Perform topological sort on a dependency graph."""
    in_degree = defaultdict(int)
    all_nodes = set(graph.keys())

    for node in graph:
        for dep in graph[node]:
            if dep in all_nodes:
                in_degree[node] += 1

    queue = [n for n in all_nodes if in_degree[n] == 0]
    queue.sort()

    result = []
    while queue:
        node = queue.pop(0)
        result.append(node)

        for other in all_nodes:
            if node in graph[other]:
                in_degree[other] -= 1
                if in_degree[other] == 0:
                    queue.append(other)
                    queue.sort()

    remaining = [n for n in all_nodes if n not in result]
    remaining.sort()
    result.extend(remaining)

    return result


def main():
    # Load schema
    schema_path = Path(__file__).parent / "adf_json_schema.json"
    output_path = Path(__file__).parent / "ADF-JSON-Schema-Analysis.md"

    with open(schema_path) as f:
        schema = json.load(f)

    definitions = schema.get("definitions", {})

    # Separate nodes and marks
    node_defs = {}
    mark_defs = {}
    other_defs = {}

    for name, definition in definitions.items():
        if name.endswith("_node"):
            node_defs[name] = definition
        elif name.endswith("_mark"):
            mark_defs[name] = definition
        else:
            other_defs[name] = definition

    # Build dependency graph
    node_deps = {}
    for name, definition in node_defs.items():
        refs = set()
        extract_refs(definition, refs)
        node_refs = {r for r in refs if r.endswith("_node") or r.endswith("_mark")}
        node_deps[name] = node_refs

    # Group by base type
    base_type_nodes = defaultdict(list)
    for name in node_defs:
        base = get_base_type(name)
        if base:
            base_type_nodes[base].append(name)

    # Build simplified dependency graph
    base_deps = {}
    for base, variants in base_type_nodes.items():
        all_deps = set()
        for variant in variants:
            for dep in node_deps.get(variant, set()):
                dep_base = get_base_type(dep)
                if dep_base and dep_base != base:
                    all_deps.add(dep_base)
        base_deps[base] = all_deps

    # Topological sort
    sorted_bases = topological_sort(base_deps)

    # Get mark bases
    mark_bases = set()
    for name in mark_defs:
        base = get_base_type(name)
        if base:
            mark_bases.add(base)

    # Build markdown content
    lines = []

    lines.append("# ADF JSON Schema Analysis")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- Total definitions: {len(definitions)}")
    lines.append(f"- Node definitions (`*_node`): {len(node_defs)}")
    lines.append(f"- Mark definitions (`*_mark`): {len(mark_defs)}")
    lines.append(f"- Other definitions: {len(other_defs)}")
    lines.append("")

    lines.append("## Implementation Order")
    lines.append("")
    lines.append("Nodes sorted by dependencies (implement dependencies first):")
    lines.append("")

    for i, base in enumerate(sorted_bases, 1):
        deps = base_deps.get(base, set())
        if deps:
            deps_str = ", ".join(sorted(deps))
            lines.append(f"{i}. **{base}** - depends on: {deps_str}")
        else:
            lines.append(f"{i}. **{base}** - no dependencies")

    lines.append("")
    lines.append("## Mark Definitions")
    lines.append("")
    lines.append(f"{len(mark_bases)} mark types:")
    lines.append("")

    for mark in sorted(mark_bases):
        lines.append(f"- {mark}")

    lines.append("")
    lines.append("## Recommended Implementation Phases")
    lines.append("")

    lines.append("### Phase 1: Base Classes")
    lines.append("")
    lines.append("- Base")
    lines.append("- BaseNode")
    lines.append("- BaseMark")
    lines.append("")

    lines.append("### Phase 2: Marks")
    lines.append("")
    lines.append("No internal dependencies, can be implemented in any order:")
    lines.append("")
    for mark in sorted(mark_bases):
        lines.append(f"- Mark{mark[0].upper()}{mark[1:]}")
    lines.append("")

    lines.append("### Phase 3: Leaf Nodes")
    lines.append("")
    lines.append("Nodes with no node dependencies:")
    lines.append("")
    leaf_nodes = [b for b in sorted_bases if not base_deps.get(b)]
    for node in leaf_nodes:
        lines.append(f"- Node{node[0].upper()}{node[1:]}")
    lines.append("")

    lines.append("### Phase 4: Composite Nodes")
    lines.append("")
    lines.append("Nodes with dependencies (implement in order):")
    lines.append("")
    composite_nodes = [b for b in sorted_bases if base_deps.get(b)]
    for node in composite_nodes:
        deps = ", ".join(sorted(base_deps[node]))
        lines.append(f"- Node{node[0].upper()}{node[1:]} - needs: {deps}")

    # Write to file
    content = "\n".join(lines)
    with open(output_path, "w") as f:
        f.write(content)

    print(f"Generated: {output_path}")


if __name__ == "__main__":
    main()
