Design Philosophy
==============================================================================


Core Concept: JSON Deserialization
------------------------------------------------------------------------------
At its core, ``atlas_doc_parser`` is a **JSON deserialization library**. Atlassian Document Format (ADF) is the rich text storage format used across Atlassian products (Confluence, Jira), stored as structured JSON documents. The primary goal of this library is to convert ADF JSON data into Python objects, enabling developers to manipulate document content in an object-oriented manner.

The core workflow:

1. **Input**: ADF JSON data (from Confluence API or Jira API)
2. **Process**: Call ``from_dict()`` method for deserialization
3. **Output**: Python dataclass objects with full type hints and attribute access


ADF Document Structure: Block-Based Nested Nodes
------------------------------------------------------------------------------
ADF is a **block-based** document format with the following characteristics:

- **Tree structure**: The entire document is a tree with ``doc`` as the root node
- **Deep nesting**: Nodes can be infinitely nested (e.g., paragraphs in lists, lists in tables)
- **Type-driven**: Each node has a ``type`` field that identifies its type

ADF defines two major categories:

1. **Node**: Represents structural elements of the document
    - Block nodes: ``paragraph``, ``heading``, ``codeBlock``, ``table``, ``bulletList``, etc.
    - Inline nodes: ``text``, ``mention``, ``emoji``, ``inlineCard``, etc.

2. **Mark**: Represents text styling and formatting
    - ``strong`` (bold), ``em`` (italic), ``link``, ``code`` (inline code), etc.

Official specification: `ADF Structure <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>`_


Python Data Model Design
------------------------------------------------------------------------------
This library uses **dataclass** as the foundation for data models, following these design principles:

**Class Hierarchy**:

- ``Base``: Base class for all data classes, providing ``from_dict()`` and ``to_dict()`` methods
- ``BaseNode``: Base class for all node classes, handling deserialization of ``type``, ``content``, ``attrs``, and ``marks`` fields
- ``BaseMark``: Base class for all mark classes, handling ``type`` and ``attrs`` fields

**Naming Conventions**:

- Node classes: ``Node{TypeName}``, e.g., ``NodeParagraph``, ``NodeHeading``
- Attribute classes: ``Node{TypeName}Attrs``, e.g., ``NodeHeadingAttrs``
- Mark classes: ``Mark{TypeName}``, e.g., ``MarkStrong``, ``MarkLink``

**Type Registry**:

All node and mark classes are registered in mapping dictionaries (``_node_type_to_class_mapping``, ``_mark_type_to_class_mapping``). The ``parse_node()`` and ``parse_mark()`` functions automatically select the correct class for deserialization based on the ``type`` field.


AI-Driven Development Pattern
------------------------------------------------------------------------------
This project adopts an **AI Agent-driven development pattern** with the following principles:

1. **Define specifications**: Establish clear code patterns and conventions
2. **Provide examples**: Create complete reference implementations
3. **Scale generation**: AI generates additional node types based on specs and examples

This pattern is particularly well-suited for ADF because:

- There are many node types (40+)
- Each node follows a similar implementation pattern
- Official documentation has a consistent structure

**Development Workflow**:

1. Read the ADF official documentation for a specific node's specification
2. Use existing node implementations as templates
3. Implement the new node's dataclass definition
4. Implement ``from_dict()`` / ``to_dict()`` / ``to_markdown()`` methods
5. Write corresponding unit tests


Future Documentation
------------------------------------------------------------------------------
This document covers the high-level design philosophy. Implementation details including:

- How to add new node types
- How to write test cases
- How to use slash commands for code generation

will be covered in subsequent documentation.
