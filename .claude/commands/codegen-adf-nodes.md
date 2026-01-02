---
description: Update s3_gen_code.py script to generate ADF node/mark dataclasses
---

Modify the code generation script at:
`./scripts/s01-adf-json-schema-analysis/s3_gen_code.py`

## Background

The `atlas_doc_parser` library parses Atlassian Document Format (ADF) JSON into Python dataclasses. The ADF schema defines ~60+ node types (paragraph, heading, table, etc.) and mark types (strong, em, link, etc.). Instead of manually writing each dataclass, we use code generation to:

1. Ensure consistency with the official ADF JSON schema
2. Reduce human error and maintenance burden
3. Automatically handle nested objects and cross-references between definitions

## Key Files

- **Script**: `./scripts/s01-adf-json-schema-analysis/s3_gen_code.py`
- **Output dir**: `./atlas_doc_parser/nodes/` (generates `mark_*.py`, `node_*.py`, `parse.py`)
- **Jinja Templates dir**: `./scripts/s01-adf-json-schema-analysis/templates/`
- **Example node file**: `./atlas_doc_parser/nodes/example_mark_background_color.py`
- **Example parse file**: `./atlas_doc_parser/nodes/example_parse.py`
- **Mixin dir**: `./atlas_doc_parser/mixins/` (manually maintained, do NOT generate)

## Requirements

### 1. Use the `adf-format-json-schema` agent skill to query schema definitions

**What**: Call `list_def` to get all definition names, then `get_def <name>` to get each definition's JSON schema.

**Why**: The ADF JSON schema is large (~5000 lines). The skill provides a clean interface to extract individual definitions without loading the entire schema into context.

### 2. Use Jinja2 templates for code generation

**What**: Store templates in `./scripts/s01-adf-json-schema-analysis/templates/` and use Jinja2 to render the output files.

**Why**: Separating templates from logic makes the code generator easier to maintain and modify.

### 3. Follow naming conventions

**What**: Convert definition names using these rules:
- `bulletList_node` → module: `node_bullet_list.py`, class: `NodeBulletList`
- `strong_mark` → module: `mark_strong.py`, class: `MarkStrong`

**Why**: Consistent naming allows predictable imports and matches Python conventions (snake_case modules, PascalCase classes).

### 4. Import mixin classes blindly

**What**: Always import the corresponding mixin class (e.g., `from ..mixins.mark_strong import MarkStrongMixin`) without checking if it exists.

**Why**: Mixin classes are manually maintained in `./atlas_doc_parser/mixins/`. If a mixin doesn't exist yet, the import will fail at test time, signaling that a human needs to create it. This is intentional—the codegen should not generate mixins.

### 5. Use `TYPE_CHECKING` for cross-definition imports

**What**: When a definition references another definition (e.g., `paragraph_node` contains `text_node`), use:
```python
import typing as T
if T.TYPE_CHECKING:
    from .node_text import NodeText
```

**Why**: Avoids circular import errors at runtime while still providing type hints for IDE support.

### 6. Create a name mapping utility function

**What**: Implement a function that maps definition names to `(module_name, class_name, attrs_class_name)`.

**Why**: Centralizes naming logic for reuse across template rendering and cross-reference resolution.
