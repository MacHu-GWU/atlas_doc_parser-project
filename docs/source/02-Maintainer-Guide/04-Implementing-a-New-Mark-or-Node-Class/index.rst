.. _implementing-a-new-mark-or-node-class:

Implementing a New Mark or Node Class
==============================================================================
This document provides a step-by-step guide for implementing a new ADF mark or node dataclass, including the rules and conventions to follow.


Quick Start: The /implement-model Command
------------------------------------------------------------------------------
For AI-assisted development, we provide a ``/implement-model`` slash command that automates most of the implementation process. It:

1. Fetches information from all three sources
2. Cross-references and validates the data
3. Generates the dataclass following all conventions
4. Updates the type mapping

**Usage:**

.. code-block:: text

    /implement-model 'Node - codeBlock    codeBlock_node    https://developer.atlassian.com/...    https://sanhehu.atlassian.net/wiki/...'

See ``.claude/commands/implement-model.md`` for detailed usage instructions.


Implementation Workflow
------------------------------------------------------------------------------


Step 1: Gather Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Consult the `atlas_doc_parser Google Sheet <https://docs.google.com/spreadsheets/d/1ETVEHWFAP-ugkIgZebLrmUF8pZ0EY6OHpyXlhdkLdwc/edit?gid=0#gid=0>`_ to find the three sources for your target type:

1. **JSON Schema Definition** - Query using the ``adf-format-json-schema`` skill
2. **Official Documentation** - Fetch the Atlassian doc URL (if available)
3. **Real Confluence Page** - Extract actual ADF JSON (if available)

**Remember:** No single source can be blindly trusted. Always cross-reference.


Step 2: Compare and Validate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Before implementing, verify consistency across sources:

- Does the schema match the official docs?
- Does the real example match the schema?
- Are there undocumented attributes in the real example?

If discrepancies exist, prioritize real behavior over documented behavior.


Step 3: Create the Dataclass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a new module following the naming convention:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Type
     - File Location
     - Class Names
   * - Mark
     - ``marks/mark_{snake_name}.py``
     - ``Mark{PascalName}``, ``Mark{PascalName}Attrs``
   * - Node
     - ``nodes/node_{snake_name}.py``
     - ``Node{PascalName}``, ``Node{PascalName}Attrs``

**Examples:**

- :mod:`~atlas_doc_parser.marks.mark_strong` - Simple mark without attrs
- :mod:`~atlas_doc_parser.marks.mark_link` - Mark with attrs
- :mod:`~atlas_doc_parser.nodes.node_text` - Simple node with marks
- :mod:`~atlas_doc_parser.nodes.node_list_item` - Node with nested content


Step 4: Register the Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
After creating the dataclass, register it in the type mapping:

- **Marks:** Add to ``MARK_TYPE_TO_CLASS_MAPPING`` in :mod:`~atlas_doc_parser.marks.parse_mark`
- **Nodes:** Add to ``NODE_TYPE_TO_CLASS_MAPPING`` in :mod:`~atlas_doc_parser.nodes.parse_node`


Implementation Rules
------------------------------------------------------------------------------
The following rules ensure consistency across all dataclass implementations.


Rule 1: Cross-Reference Type Hints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When the JSON schema contains ``$ref`` (references to other definitions), you must use cross-reference type hints with forward references.

**How to identify:** Look for ``$ref`` in the schema:

.. code-block:: json

    "content": { "items": { "$ref": "#/definitions/listItem_node" } }

**Implementation pattern:**

.. code-block:: python

    import typing as T

    if T.TYPE_CHECKING:  # pragma: no cover
        from .node_paragraph import NodeParagraph
        from .node_code_block import NodeCodeBlock

    @dataclasses.dataclass(frozen=True)
    class NodeListItem(BaseNode):
        content: list[T.Union["NodeParagraph", "NodeCodeBlock"]] = OPT

**Key points:**

- Use quoted strings (``"ClassName"``) for forward references
- Import under ``TYPE_CHECKING`` to avoid circular imports
- Never use ``BaseNode`` or ``BaseMark`` as generic types

See :mod:`~atlas_doc_parser.nodes.node_list_item` for a complete example.


Rule 2: Required vs Optional Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Match the JSON schema's ``required`` array when setting default values:

- **Required fields** → use ``REQ`` as default
- **Optional fields** → use ``OPT`` as default

**Check both levels:**

1. Top-level fields (``attrs``, ``content``, ``marks``)
2. Attrs class fields (each individual attribute)

.. code-block:: python

    # Schema: "required": ["type", "attrs"]
    # Attrs: "required": ["text", "color"]

    class NodeStatusAttrs(Base):
        text: str = REQ      # Required in attrs
        color: str = REQ     # Required in attrs
        localId: str = OPT   # Optional in attrs

    class NodeStatus(BaseNode):
        type: str = TypeEnum.status.value
        attrs: NodeStatusAttrs = REQ  # Required at top level

See :mod:`~atlas_doc_parser.nodes.node_status` for a complete example.


Rule 3: Do NOT Use T.Optional
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Never use ``T.Optional[...]`` for optional attributes. The ``OPT`` sentinel value already indicates optionality:

.. code-block:: python

    # ✅ CORRECT
    class NodeExampleAttrs(Base):
        url: str = OPT
        width: int = OPT

    # ❌ WRONG - redundant and inconsistent
    class NodeExampleAttrs(Base):
        url: T.Optional[str] = OPT
        width: T.Optional[int] = OPT


Rule 4: Use TypeEnum for the type Field
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For the ``type`` field, always use :mod:`~atlas_doc_parser.type_enum`:

.. code-block:: python

    # ✅ CORRECT
    class NodeHardBreak(BaseNode):
        type: str = TypeEnum.hardBreak.value

    # ❌ WRONG - do not use T.Literal for type field
    class NodeHardBreak(BaseNode):
        type: T.Literal["hardBreak"] = "hardBreak"

For **other** enum fields (not ``type``), use ``T.Literal``:

.. code-block:: python

    class NodeMediaSingleAttrs(Base):
        layout: T.Literal["wide", "center", "full-width"] = OPT


Reference Implementations
------------------------------------------------------------------------------
Study these examples to understand different patterns:

**Simple marks:**

- :mod:`~atlas_doc_parser.marks.mark_code` - No attrs
- :mod:`~atlas_doc_parser.marks.mark_strong` - No attrs
- :mod:`~atlas_doc_parser.marks.mark_link` - With attrs

**Simple nodes:**

- :mod:`~atlas_doc_parser.nodes.node_text` - Inline node with marks
- :mod:`~atlas_doc_parser.nodes.node_hard_break` - Minimal node
- :mod:`~atlas_doc_parser.nodes.node_rule` - Block node

**Nodes with content:**

- :mod:`~atlas_doc_parser.nodes.node_paragraph` - Single content type
- :mod:`~atlas_doc_parser.nodes.node_list_item` - Multiple content types (Union)
- :mod:`~atlas_doc_parser.nodes.node_doc` - Root document node

**Nodes with attrs:**

- :mod:`~atlas_doc_parser.nodes.node_heading` - Simple attrs
- :mod:`~atlas_doc_parser.nodes.node_code_block` - Optional attrs
- :mod:`~atlas_doc_parser.nodes.node_media` - Complex attrs with marks
