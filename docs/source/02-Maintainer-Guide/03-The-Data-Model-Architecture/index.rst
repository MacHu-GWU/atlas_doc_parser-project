The Data Model Architecture
==============================================================================

This document explains the foundational classes that all ADF marks and nodes inherit from, and how they provide the core functionality for serialization, deserialization, and Markdown conversion.


One Definition, One Class
------------------------------------------------------------------------------
Each definition in the ADF JSON schema corresponds to:

- **One Python module** (e.g., ``node_paragraph.py``, ``mark_strong.py``)
- **One Python class** (e.g., ``NodeParagraph``, ``MarkStrong``)

In special cases, multiple schema definitions may map to a single class when they represent variants of the same concept. For example, different media type variants might share the same ``NodeMedia`` class.

The class hierarchy is:

.. code-block:: text

    Base
    └── BaseMarkOrNode
        ├── BaseMark      # For text formatting (strong, em, link, etc.)
        └── BaseNode      # For document structure (paragraph, heading, etc.)

Every mark and node has a ``type`` field that identifies what kind of element it is
(e.g., ``"paragraph"``, ``"strong"``). The valid type values are defined in the
:mod:`~atlas_doc_parser.type_enum` module as the ``TypeEnum`` enumeration. When
implementing a new dataclass, always use ``TypeEnum.xxx.value`` for the ``type``
field's default value.


Class Hierarchy
------------------------------------------------------------------------------


Base Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``Base`` class (in ``atlas_doc_parser.mark_or_node``) provides common functionality for all ADF dataclasses:

**Key Methods:**

- ``from_dict(dct)``: Construct an instance from a dictionary. Uses defensive programming to ignore unknown fields, ensuring forward compatibility when Atlassian adds new fields.
- ``to_dict()``: Serialize the instance back to a dictionary, suitable for JSON encoding.
- ``get_fields()``: Returns cached field information for performance.


BaseMark Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The ``BaseMark`` class represents text formatting marks like bold, italic, links, etc.

**from_dict() Behavior:**

Marks have a simpler structure than nodes. The ``from_dict()`` method only needs to handle:

1. The ``type`` field (e.g., ``"strong"``, ``"em"``)
2. Optional ``attrs`` field (e.g., link URL, text color)

It does NOT recursively parse nested content because marks don't contain child nodes.

**to_markdown() Behavior:**

.. code-block:: python

    def to_markdown(self, text: str) -> str:
        return text  # Default: return text unchanged

The default implementation returns the input text unchanged. This design reflects that:

1. **The primary goal of to_markdown is content extraction, not formatting.** In the AI era, we're converting ADF to Markdown primarily to extract textual content for LLMs, RAG systems, and knowledge bases. Preserving formatting is secondary.
2. **When in doubt, preserve content without formatting.** If a mark type doesn't have a standard Markdown equivalent, we simply return the raw text rather than inventing custom syntax.
3. **Use native Markdown only.** We prefer standard Markdown syntax (e.g., ``**bold**``, ``*italic*``). Dialect-specific extensions like GitHub-flavored Markdown tables are avoided when possible.

Subclasses override this method to apply formatting. For example, ``MarkStrong.to_markdown("text")`` returns ``"**text**"``.


BaseNode Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``BaseNode`` class represents document structure elements like paragraphs, headings, lists, tables, etc.

**from_dict() Behavior:**

Nodes have a more complex structure. The ``from_dict()`` method handles:

1. The ``type`` field (e.g., ``"paragraph"``, ``"heading"``)
2. Optional ``attrs`` field (node-specific attributes)
3. Optional ``content`` field (child nodes) - **recursively parsed**
4. Optional ``marks`` field (text formatting) - **recursively parsed**

The key difference from ``BaseMark.from_dict()`` is the recursive parsing of ``content`` and ``marks`` using ``parse_node()`` and ``parse_mark()`` respectively.

**to_markdown() Behavior:**

.. code-block:: python

    def to_markdown(self, ignore_error: bool = False) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__} has not implemented ``to_markdown()``"
        )

The default implementation raises ``NotImplementedError``. This is intentional:

1. **Fail fast during development.** When developing new node types, we want to immediately discover which nodes haven't implemented ``to_markdown()`` rather than silently producing empty output.

2. **The ignore_error parameter provides an escape hatch.** In production, users can pass ``ignore_error=True`` to gracefully skip nodes that fail to convert. This flag propagates recursively to all nested nodes.

3. **Error handling is explicit.** The library user decides whether to fail fast (for debugging) or degrade gracefully (for production).

Subclasses must override this method. The ``ignore_error`` parameter should be passed down to any nested ``to_markdown()`` calls for consistent behavior.


Markdown Helper Functions
------------------------------------------------------------------------------
The ``atlas_doc_parser.markdown_helpers`` module provides utility functions used by node classes to implement ``to_markdown()``.


strip_double_empty_line()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def strip_double_empty_line(text: str, n: int = 3) -> str

**Purpose:** Remove excessive consecutive blank lines from the output.

When converting block-level nodes, many nodes add blank lines before/after themselves to ensure proper Markdown rendering. This can result in 3+ consecutive blank lines, which looks ugly. This function normalizes the output to at most one blank line (two newlines).

**Usage:** Called internally by ``doc_content_to_markdown()`` to clean up the final output.


content_to_markdown()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    def content_to_markdown(
        content: list[T_NODE],
        concat: str = "",
        ignore_error: bool = False,
    ) -> str

**Purpose:** Recursively convert a list of child nodes to concatenated Markdown.

This is the workhorse function for converting nested content. It:

1. Iterates through all child nodes
2. Calls ``to_markdown()`` on each
3. Concatenates the results

**Usage:** Used by most nodes that have a ``content`` field (paragraphs, headings, list items, etc.).

**Example:**

.. code-block:: python

    # In NodeParagraph.to_markdown():
    md = content_to_markdown(self.content, ignore_error=ignore_error)


doc_content_to_markdown()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    def doc_content_to_markdown(
        content: list[T_NODE],
        concat: str = "\n",
        ignore_error: bool = False,
    ) -> str

**Purpose:** Convert document-level (root) content to Markdown with proper block separation.

This function is specifically for the ``NodeDoc`` root node. It differs from ``content_to_markdown()`` in that:

1. Joins blocks with newlines (not empty string)
2. Adds extra blank lines around lists and code blocks for proper rendering
3. Cleans up excessive blank lines in the final output

**Usage:** Called by ``NodeDoc.to_markdown()`` only.


add_style_to_markdown()
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    def add_style_to_markdown(md: str, node: T_NODE) -> str

**Purpose:** Apply mark formatting to Markdown text.

When a node has marks (e.g., bold + italic text), this function applies each mark's formatting in sequence:

1. Start with plain text: ``"hello"``
2. Apply strong mark: ``"**hello**"``
3. Apply em mark: ``"***hello***"``

**Usage:** Used by nodes that support text formatting (``NodeText``, ``NodeHeading``, etc.).

**Example:**

.. code-block:: python

    # In NodeText.to_markdown():
    md = self.text
    md = add_style_to_markdown(md, self)
    return md


Summary
------------------------------------------------------------------------------
The base classes provide a consistent foundation for all ADF types:

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - Feature
     - BaseMark
     - BaseNode
   * - from_dict()
     - Parses ``type`` and ``attrs``
     - Parses ``type``, ``attrs``, ``content``, ``marks`` (recursive)
   * - to_dict()
     - Serializes all fields
     - Serializes all fields (recursive)
   * - to_markdown()
     - Returns text unchanged (subclasses add formatting)
     - Raises NotImplementedError (subclasses must implement)
   * - ignore_error
     - N/A
     - Propagates to nested calls for graceful degradation

The helper functions handle common patterns so that individual node/mark implementations can focus on their specific conversion logic.
