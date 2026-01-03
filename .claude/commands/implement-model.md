---
description: Implement ADF node/mark dataclass from spec
---

# Task

Implement a Python dataclass for the given Atlassian Document Format (ADF) model.

# Input

**Arg 1 (required):** Tab-separated string with 2-4 fields:

```
{Object Name}<TAB>{Def Name}[<TAB>{Atlassian Doc URL}[<TAB>{Example Confluence Page URL}]]
```

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| Object Name | ✓ | Human-readable name | `Mark - backgroundColor` or `Node - codeBlock` |
| Def Name | ✓ | Schema definition name | `backgroundColor_mark` or `codeBlock_node` |
| Atlassian Doc URL | | Official doc page (may not exist) | `https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/backgroundColor/` |
| Example Page URL | | Confluence page with example (may not exist) | `https://sanhehu.atlassian.net/wiki/...` |

**Note:** Only Object Name and Def Name are guaranteed. If Atlassian Doc URL or Example Page URL is missing, rely primarily on the JSON schema.

**Arg 2 (optional):** Additional requirements or instructions.

# User Input

$ARGUMENTS

# Instructions

## Step 1: Gather Information from Available Sources

**IMPORTANT**:
- Do NOT blindly trust any single source. Cross-reference all available sources to ensure accuracy.
- If Atlassian Doc URL or Example Page URL is not provided, **JSON Schema is the primary source of truth**.

### Source 1 - JSON Schema (Always Available)
Use `adf-format-json-schema` agent skill:
- Run `list_def` to verify the Def Name exists
- Run `get_def {Def Name}` to get the JSON schema definition

### Source 2 - Official Documentation (If Provided)
Fetch the Atlassian Doc URL to understand:
- The model's purpose and usage
- Expected attributes and their types
- Official examples (note: may be minimal or incomplete)

Skip this step if Atlassian Doc URL is not provided.

### Source 3 - Real-World Example (If Provided)
Use `adf-json-example` agent skill to get actual ADF JSON from the Example Confluence Page using the given ${Example Page URL}

This shows how the model is actually used in practice.

Skip this step if Example Page URL is not provided.

## Step 2: Compare and Validate

Cross-reference all three sources:
- Does the schema match the official docs?
- Does the real example match the schema?
- Are there attributes in the example not documented?

**If discrepancies exist or you're unsure, ASK the user before implementing.**

## Step 3: Implement Dataclass

Create `mark_*.py` or `node_*.py` file with:
- Only the dataclass schema definition
- Do NOT implement `to_markdown()` or other methods (maintained by human)

### Important Implementation Rules

#### Rule 1: Cross-Reference Type Hints (`$ref` in JSON Schema)

**CRITICAL:** When JSON schema contains `$ref` anywhere (in `content`, `marks`, or nested `attrs`), you MUST use cross-reference type hints.

**How to identify:** Look for `$ref` in the schema output:
```json
"content": { "items": { "$ref": "#/definitions/listItem_node" } }
"marks": { "items": { "anyOf": [{ "$ref": "#/definitions/link_mark" }, ...] } }
```

**Implementation pattern:**
```python
import typing as T

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_list_item import NodeListItem
    from ..marks.mark_link import MarkLink

@dataclasses.dataclass(frozen=True)
class NodeExample(BaseNode):
    content: list["NodeListItem"] = OPT  # $ref → cross-reference
    marks: list["MarkLink"] = OPT        # $ref → cross-reference
```

**For multiple refs (anyOf/oneOf):**
```python
content: list[
    T.Union[
        "NodeParagraph",
        "NodeCodeBlock",
        "NodeBulletList",
    ]
] = OPT
```

**Key points:**
- `$ref` = cross-reference type hint required (never use `BaseNode` or `BaseMark`)
- Add imports even if module doesn't exist yet - `TYPE_CHECKING` prevents runtime errors
- Use quoted strings (`"ClassName"`) for forward references
- Derive module name: `MarkLink` → `mark_link`, `NodeParagraph` → `node_paragraph`

See `./atlas_doc_parser/nodes/node_list_item.py` for a complete example with multiple refs.

#### Rule 2: Required vs Optional Fields - Use `REQ` and `OPT` Correctly

**CRITICAL:** Match the JSON schema's `required` array when setting default values:

- **Required fields** → use `REQ` as default value
- **Optional fields** → use `OPT` as default value

```python
# JSON schema shows: "required": ["timestamp"], "properties": {"timestamp": {...}, "localId": {...}}

# ✅ CORRECT - match schema's required array
class NodeDateAttrs(Base):
    timestamp: str = REQ    # In required array → REQ
    localId: str = OPT      # NOT in required array → OPT
```

**Check both levels:**

1. **Top-level node/mark fields** - check if `attrs`, `content`, `text`, `marks` are in the top-level `required` array
2. **Attrs class fields** - check if each attr field is in the attrs object's `required` array

```python
# JSON schema shows:
# - Top level: "required": ["type", "attrs"]
# - Attrs: "required": ["text", "color"]

# ✅ CORRECT
class NodeStatusAttrs(Base):
    text: str = REQ         # Required in attrs
    color: str = REQ        # Required in attrs
    localId: str = OPT      # Optional in attrs

class NodeStatus(BaseNode):
    type: str = TypeEnum.status.value
    attrs: NodeStatusAttrs = REQ  # Required at top level
```

**For `anyOf` schemas:** When attrs has multiple variants (anyOf), use OPT for fields that are only required in some variants, since the Python class must accept all variants.

#### Rule 3: Optional Attributes - Do NOT Use `T.Optional`

**NEVER use `T.Optional[...]`** for optional attributes. The `OPT` sentinel value already indicates optionality:

```python
# ✅ CORRECT - use direct type with OPT default
class NodeExampleAttrs(Base):
    url: str = OPT
    width: int = OPT
    color: str = OPT

# ❌ WRONG - do not use T.Optional
class NodeExampleAttrs(Base):
    url: T.Optional[str] = OPT      # NO!
    width: T.Optional[int] = OPT    # NO!
```

**Exception:** Only use `T.Optional` if the JSON schema explicitly specifies `nullable: true` (which is rare).

#### Rule 4: Enum Types - Use `TypeEnum` for `type` Field

When JSON schema shows an enum for a string field (e.g., `"enum": ["hardBreak"]`):

1. **First check if it's the `type` field** - if yes, use `TypeEnum.xxx.value`
2. **For other fields** - use `T.Literal[...]`

```python
# JSON schema shows: "type": { "enum": ["hardBreak"] }

# ✅ CORRECT - use TypeEnum for the `type` field
class NodeHardBreak(BaseNode):
    type: str = TypeEnum.hardBreak.value

# ❌ WRONG - do not use T.Literal for the `type` field
class NodeHardBreak(BaseNode):
    type: T.Literal["hardBreak"] = "hardBreak"  # NO!
```

```python
# JSON schema shows: "layout": { "enum": ["wide", "center", "full-width"] }

# ✅ CORRECT - use T.Literal for non-type enum fields
class NodeMediaSingleAttrs(Base):
    layout: T.Literal["wide", "center", "full-width"] = OPT
```

## Step 4: Update Type Mapping

After creating the dataclass file, update the type-to-class mapping:

- **For Marks**: Update `MARK_TYPE_TO_CLASS_MAPPING` in `./atlas_doc_parser/marks/parse_mark.py`
- **For Nodes**: Update `NODE_TYPE_TO_CLASS_MAPPING` in `./atlas_doc_parser/nodes/parse_node.py`

This mapping allows the parser to instantiate the correct class based on the `type` field in ADF JSON.

# Output Conventions

| Object Name Pattern | File Location | Class Names |
|---------------------|---------------|-------------|
| `Mark - {name}` | `./atlas_doc_parser/marks/mark_{snake_name}.py` | `Mark{PascalName}`, `Mark{PascalName}Attrs` |
| `Node - {name}` | `./atlas_doc_parser/nodes/node_{snake_name}.py` | `Node{PascalName}`, `Node{PascalName}Attrs` |

**Example:**
- `Mark - backgroundColor` → `mark_background_color.py` → `MarkBackgroundColor`
- `Node - codeBlock` → `node_code_block.py` → `NodeCodeBlock`

# Reference Implementation

See the following source code for complete examples:

**Basic examples:**
- `./atlas_doc_parser/marks/mark_background_color.py` - simple mark with attrs
- `./atlas_doc_parser/marks/mark_code.py` - mark without attrs
- `./atlas_doc_parser/marks/mark_link.py` - mark with multiple attrs
- `./atlas_doc_parser/nodes/node_text.py` - simple node
- `./atlas_doc_parser/nodes/node_list_item.py` - node with content

**Cross-reference type hint examples (Rule 1):**
- `./atlas_doc_parser/nodes/node_list_item.py` - multiple content refs with `T.Union`
- `./atlas_doc_parser/nodes/node_text.py` - multiple marks refs with `T.Union`
- `./atlas_doc_parser/nodes/node_media.py` - marks with `T.Union`
