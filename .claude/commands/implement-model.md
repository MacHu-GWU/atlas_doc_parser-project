---
description: Implement ADF node/mark dataclass from spec
---

# Task

Implement a Python dataclass for the given Atlassian Document Format (ADF) model.

# Input

**Arg 1 (required):** Tab-separated string with 4 fields:

```
{Object Name}<TAB>{Def Name}<TAB>{Atlassian Doc URL}<TAB>{Example Confluence Page URL}
```

| Field | Description | Example |
|-------|-------------|---------|
| Object Name | Human-readable name | `Mark - backgroundColor` or `Node - codeBlock` |
| Def Name | Schema definition name | `backgroundColor_mark` or `codeBlock_node` |
| Atlassian Doc URL | Official doc page | `https://developer.atlassian.com/cloud/jira/platform/apis/document/marks/backgroundColor/` |
| Example Page URL | Confluence page with example | `https://sanhehu.atlassian.net/wiki/...` |

**Arg 2 (optional):** Additional requirements or instructions.

# User Input

$ARGUMENTS

# Instructions

## Step 1: Gather Information from Three Sources

**IMPORTANT**: Do NOT blindly trust any single source. Cross-reference all three to ensure accuracy.

### Source 1 - JSON Schema
Use `adf-format-json-schema` agent skill:
- Run `list_def` to verify the Def Name exists
- Run `get_def {Def Name}` to get the JSON schema definition

### Source 2 - Official Documentation
Fetch the Atlassian Doc URL to understand:
- The model's purpose and usage
- Expected attributes and their types
- Official examples (note: may be minimal or incomplete)

### Source 3 - Real-World Example
Use `adf-json-example` agent skill to get actual ADF JSON from the Example Confluence Page using the given ${Example Page URL}

This shows how the model is actually used in practice.

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

- `./atlas_doc_parser/marks/mark_background_color.py`
- `./atlas_doc_parser/marks/mark_code.py`
- `./atlas_doc_parser/marks/mark_em.py`
- `./atlas_doc_parser/marks/mark_link.py`
