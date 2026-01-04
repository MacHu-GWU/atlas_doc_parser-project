Graceful Handling of Unimplemented Types
==============================================================================

Overview
------------------------------------------------------------------------------

The Atlassian Document Format (ADF) is a rich specification with many node and mark types. As a library that evolves incrementally, ``atlas_doc_parser`` may not implement all ADF types at any given time. This document explains how the library gracefully handles unimplemented types during parsing.


Design Philosophy
------------------------------------------------------------------------------

The library follows a **progressive implementation** approach:

1. **Parse what we can**: When encountering an ADF document, the parser deserializes all implemented node and mark types into Python objects.

2. **Skip what we can't**: Unimplemented types are silently skipped rather than causing the entire parsing operation to fail.

3. **Inform the user**: When an unimplemented type is encountered, a warning is logged to inform users which types are missing. This helps users identify gaps and submit feature requests.

4. **Fail on real errors**: Actual parsing errors (malformed data, type mismatches, etc.) are still raised as exceptions. Only missing type registrations are skipped.

This design ensures that:

- Users can work with partial ADF documents even if the library doesn't support all types yet
- The library can evolve incrementally without breaking existing functionality
- Users are informed about which types need implementation


Error Handling Behavior
------------------------------------------------------------------------------

When to Skip Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Errors are **skipped** only when:

- A node type is not registered in ``NODE_TYPE_TO_CLASS_MAPPING``
- A mark type is not registered in ``MARK_TYPE_TO_CLASS_MAPPING``

In these cases, the unimplemented element is simply omitted from the parsed result.

When to Raise Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Errors are **raised** normally when:

- The ``from_dict()`` method of a dataclass fails (malformed attributes, type errors, etc.)
- Any other exception occurs during parsing (network errors, JSON decode errors, etc.)
- The ADF structure is invalid (missing required fields, wrong types, etc.)

This distinction ensures that genuine bugs and data issues are surfaced while allowing the library to handle incomplete implementations gracefully.


Implementation Details
------------------------------------------------------------------------------

Key Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The graceful handling mechanism involves several components:

1. **Exception Class**: ``atlas_doc_parser.exc.UnimplementedTypeError``

   A custom exception raised when a type is not found in the registry. It carries the type name and category (node or mark) for informative error messages.

2. **Parse Functions**: ``parse_node()`` and ``parse_mark()``

   Located in ``atlas_doc_parser.nodes.parse_node`` and ``atlas_doc_parser.marks.parse_mark`` respectively. These functions look up the type in their respective mapping dictionaries. If the type is not found, they raise ``UnimplementedTypeError`` instead of letting the ``KeyError`` propagate.

3. **Base Class Handler**: ``BaseNode.from_dict()``

   Located in ``atlas_doc_parser.mark_or_node``. This method catches ``UnimplementedTypeError`` specifically when parsing ``content`` (child nodes) and ``marks``. When caught, it skips the unimplemented element and continues parsing the remaining elements.

4. **Warning Control**: ``settings.WARN_UNIMPLEMENTED_TYPE``

   A module-level boolean flag in ``atlas_doc_parser.settings`` that controls whether warnings are logged for unimplemented types. Default is ``True``.

Code Flow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When parsing a document::

    NodeDoc.from_dict(data)
        |
        +-- For each item in content:
        |       |
        |       +-- parse_node(item_data)
        |               |
        |               +-- Type not in NODE_TYPE_TO_CLASS_MAPPING?
        |               |       |
        |               |       +-- Raise UnimplementedTypeError
        |               |
        |               +-- Type found?
        |                       |
        |                       +-- Call NodeClass.from_dict(item_data)
        |
        +-- Catch UnimplementedTypeError?
        |       |
        |       +-- Log warning (if WARN_UNIMPLEMENTED_TYPE is True)
        |       +-- Skip this item, continue with next
        |
        +-- Catch other exceptions?
                |
                +-- Re-raise (fail normally)


Usage Examples
------------------------------------------------------------------------------

Default Behavior (Warnings Enabled)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from atlas_doc_parser.nodes.node_doc import NodeDoc

    # Parse a document that contains an unimplemented node type
    data = {
        "version": 1,
        "type": "doc",
        "content": [
            {"type": "bodiedExtension", "attrs": {...}},  # Not implemented
            {"type": "paragraph", "content": [{"type": "text", "text": "Hello"}]}
        ]
    }

    doc = NodeDoc.from_dict(data)
    # WARNING logged: Node type 'bodiedExtension' is not yet implemented...
    # doc.content contains only the paragraph (bodiedExtension was skipped)

Disabling Warnings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import atlas_doc_parser.settings as settings

    # Disable warnings for unimplemented types
    settings.WARN_UNIMPLEMENTED_TYPE = False

    # Now parse silently
    doc = NodeDoc.from_dict(data)
    # No warning logged, unimplemented types still skipped


Testing
------------------------------------------------------------------------------

The graceful handling mechanism is tested in ``tests/nodes/test_nodes_node_doc.py`` with the ``test_node_doc_with_unimplemented_model`` test case. This test uses a Confluence page that intentionally contains an unimplemented node type (``bodiedExtension``) to verify that:

1. Parsing completes without raising an exception
2. The unimplemented node is skipped
3. Other nodes in the document are parsed correctly


Contributing New Types
------------------------------------------------------------------------------

When a user encounters an unimplemented type, the warning message directs them to submit an issue at:

https://github.com/MacHu-GWU/atlas_doc_parser-project/issues

To implement a new type:

1. Create the dataclass in the appropriate module (``nodes/`` or ``marks/``)
2. Register the type in the mapping dictionary (``NODE_TYPE_TO_CLASS_MAPPING`` or ``MARK_TYPE_TO_CLASS_MAPPING``)
3. Add tests for the new type

See the :doc:`/02-Maintainer-Guide/index` for detailed instructions on implementing new types.
