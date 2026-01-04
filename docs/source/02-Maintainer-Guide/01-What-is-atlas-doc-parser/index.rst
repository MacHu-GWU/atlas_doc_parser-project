What is atlas_doc_parser?
==============================================================================

Introduction
------------------------------------------------------------------------------
``atlas_doc_parser`` is a Python library for parsing and transforming `Atlassian Document Format (ADF) <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>`_ - the rich text format used in Confluence pages and Jira issue fields.


The Problem
------------------------------------------------------------------------------
Atlassian products like Confluence and Jira store rich text content in a proprietary JSON format called ADF (Atlassian Document Format). When you retrieve a Confluence page or Jira ticket via API, the body content is returned as a complex nested JSON structure.

For example, a simple paragraph with bold text looks like this in ADF::

    {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": "Hello ",
                    },
                    {
                        "type": "text",
                        "text": "world",
                        "marks": [{"type": "strong"}]
                    }
                ]
            }
        ]
    }

Working directly with this raw JSON is cumbersome. You need to:

- Navigate deeply nested structures
- Handle dozens of different node and mark types
- Deal with optional attributes and edge cases
- Convert to human-readable formats for processing


The Solution
------------------------------------------------------------------------------
``atlas_doc_parser`` provides a clean abstraction layer:

1. **Parse**: Deserialize ADF JSON into strongly-typed Python dataclasses
2. **Navigate**: Work with an Abstract Syntax Tree (AST) structure with proper types
3. **Transform**: Convert to other formats (currently Markdown, more to come)

.. code-block:: python

    from atlas_doc_parser.nodes.node_doc import NodeDoc

    # Parse ADF JSON into Python objects
    doc = NodeDoc.from_dict(adf_json)

    # Now you have a proper AST
    for node in doc.content:
        if node.type == "paragraph":
            for child in node.content:
                print(child.text)

    # Convert to Markdown
    markdown = doc.to_markdown()


Why Markdown?
------------------------------------------------------------------------------
In the era of AI and Large Language Models, knowledge stored in Confluence and Jira needs to be accessible for:

- **AI Training**: Feed structured documentation to language models
- **RAG Systems**: Build retrieval-augmented generation pipelines
- **Knowledge Bases**: Create searchable, AI-friendly documentation
- **Content Migration**: Move content between platforms

Markdown is the lingua franca for these use cases - it's plain text, universally supported, and preserves document structure while remaining human-readable.


Future Directions
------------------------------------------------------------------------------
While ``to_markdown()`` is the primary transformation today, the architecture supports adding more conversions:

- ``to_html()`` - Direct HTML output
- ``to_rst()`` - ReStructuredText for Sphinx documentation
- ``to_docx()`` - Microsoft Word documents
- ``to_pdf()`` - PDF generation
- Custom transformations via visitor pattern

The core value is the parsed AST - once you have structured Python objects, you can transform them to any format you need.
