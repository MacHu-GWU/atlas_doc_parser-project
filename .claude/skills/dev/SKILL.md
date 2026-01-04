---
name: dev
description: Maintainer guide for atlas_doc_parser development. Use when implementing ADF marks/nodes, understanding codebase architecture, or writing tests.
---

# atlas_doc_parser Maintainer Guide

This skill provides guidance for developing and maintaining the atlas_doc_parser library.

## Available Topics

Read the specific document when you need detailed information:

| Topic | Document                                                                                                                             | When to Read |
|-------|--------------------------------------------------------------------------------------------------------------------------------------|--------------|
| **Overview** | [01-What-is-atlas-doc-parser](docs/source/02-Maintainer-Guide/01-What-is-atlas-doc-parser/index.rst)                                 | Understanding project purpose and design philosophy |
| **Three Sources** | [02-Cross-Referencing](docs/source/02-Maintainer-Guide/02-Cross-Referencing-Three-Sources-of-Truth/index.rst)                        | Learning about JSON schema, docs, and real Confluence pages |
| **Base Classes** | [03-The-Base-Class](docs/source/02-Maintainer-Guide/03-The-Base-Class/index.rst)                                                     | Understanding Base, BaseMark, BaseNode, and markdown helpers |
| **Implementation** | [04-Per-Mark-Node-Class](docs/source/02-Maintainer-Guide/04-Per-Mark-Node-Class/index.rst)                                           | Implementing a new mark or node dataclass |
| **Testing** | [05-How-to-Test](docs/source/02-Maintainer-Guide/05-How-to-Test/index.rst)                                                           | Writing tests for marks and nodes |
| **Error Handling** | [06-Graceful-Handling-of-Unimplemented-Types](docs/source/02-Maintainer-Guide/06-Graceful-Handling-of-Unimplemented-Types/index.rst) | How unimplemented types are handled gracefully |

## Quick Reference

- **Implement new mark/node**: Read "Implementation" then "Testing"
- **Understand architecture**: Read "Overview" then "Base Classes"
- **Debug parsing issues**: Read "Three Sources" and "Error Handling"

## Related Skills

- `adf-format-json-schema` - Query ADF JSON schema definitions
- `adf-json-example` - Fetch real ADF JSON from Confluence pages
- `implement-model` - Automated implementation workflow
