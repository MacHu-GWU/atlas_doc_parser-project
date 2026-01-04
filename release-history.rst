.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


1.0.1 (2026-01-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Major Refactor**

This release represents a significant architectural overhaul focused on reliability, maintainability, and AI-native development practices.

**Architecture Changes**

- Refactored from monolithic ``model.py`` to modular structure with separate ``marks/`` and ``nodes/`` directories
- Each ADF type now has its own dedicated module (e.g., ``node_paragraph.py``, ``mark_strong.py``)
- Added code generation for ``api.py`` to ensure consistent public API exports
- Introduced ``TypeEnum`` for type-safe ADF type handling
- Added graceful error handling: unimplemented types are now skipped with optional warnings instead of crashing

**New Mark Types**

- :class:`~atlas_doc_parser.marks.mark_alignment.MarkAlignment`
- :class:`~atlas_doc_parser.marks.mark_border.MarkBorder`
- :class:`~atlas_doc_parser.marks.mark_breakout.MarkBreakout`
- :class:`~atlas_doc_parser.marks.mark_data_consumer.MarkDataConsumer`
- :class:`~atlas_doc_parser.marks.mark_fragment.MarkFragment`

**New Node Types**

- :class:`~atlas_doc_parser.nodes.node_caption.NodeCaption`
- :class:`~atlas_doc_parser.nodes.node_decision_item.NodeDecisionItem`
- :class:`~atlas_doc_parser.nodes.node_decision_list.NodeDecisionList`
- :class:`~atlas_doc_parser.nodes.node_embed_card.NodeEmbedCard`
- :class:`~atlas_doc_parser.nodes.node_extension.NodeExtension`
- :class:`~atlas_doc_parser.nodes.node_media_inline.NodeMediaInline`

**Testing Improvements**

- Comprehensive test coverage using real Confluence page data
- Two-layer testing architecture: ``PageSample`` (page-level) and ``AdfSample`` (element-level)
- JMESPath-based element extraction for precise testing
- Round-trip serialization tests for all implemented types

**Documentation**

- Complete maintainer guide with 5 sections:
    - Project overview and design philosophy
    - Cross-referencing three sources of truth (JSON schema, official docs, real pages)
    - Base class architecture and markdown helpers
    - Step-by-step guide for implementing new marks/nodes
    - Testing workflow documentation
- User-facing getting started guide with practical examples
- AI-consumable documentation structure

**AI-Native Development**

- Claude Code skills for development workflow:
    - ``/dev`` - Maintainer guide quick reference
    - ``/adf-format-json-schema`` - Query ADF JSON schema
    - ``/adf-json-example`` - Fetch real ADF from Confluence
    - ``/implement-model`` - Automated implementation workflow


0.1.2 (2025-03-03)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Made it open source and publish to PyPI


0.1.1 (2025-01-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release (GitHub Relase only)
- Add support to export to Markdown
- Support the following mark and node type:
    - :class:`~atlas_doc_parser.model.MarkBackGroundColor`
    - :class:`~atlas_doc_parser.model.MarkCode`
    - :class:`~atlas_doc_parser.model.MarkEm`
    - :class:`~atlas_doc_parser.model.MarkLink`
    - :class:`~atlas_doc_parser.model.MarkStrike`
    - :class:`~atlas_doc_parser.model.MarkStrong`
    - :class:`~atlas_doc_parser.model.MarkSubSup`
    - :class:`~atlas_doc_parser.model.MarkTextColor`
    - :class:`~atlas_doc_parser.model.MarkUnderLine`
    - :class:`~atlas_doc_parser.model.MarkIndentation`
    - :class:`~atlas_doc_parser.model.NodeBlockCard`
    - :class:`~atlas_doc_parser.model.NodeBlockQuote`
    - :class:`~atlas_doc_parser.model.NodeBulletList`
    - :class:`~atlas_doc_parser.model.NodeCodeBlock`
    - :class:`~atlas_doc_parser.model.NodeDate`
    - :class:`~atlas_doc_parser.model.NodeDoc`
    - :class:`~atlas_doc_parser.model.NodeEmoji`
    - :class:`~atlas_doc_parser.model.NodeExpand`
    - :class:`~atlas_doc_parser.model.NodeHardBreak`
    - :class:`~atlas_doc_parser.model.NodeHeading`
    - :class:`~atlas_doc_parser.model.NodeInlineCard`
    - :class:`~atlas_doc_parser.model.NodeListItem`
    - :class:`~atlas_doc_parser.model.NodeMedia`
    - :class:`~atlas_doc_parser.model.NodeMediaGroup`
    - :class:`~atlas_doc_parser.model.NodeMediaSingle`
    - :class:`~atlas_doc_parser.model.NodeMention`
    - :class:`~atlas_doc_parser.model.NodeNestedExpand`
    - :class:`~atlas_doc_parser.model.NodeOrderedList`
    - :class:`~atlas_doc_parser.model.NodePanel`
    - :class:`~atlas_doc_parser.model.NodeParagraph`
    - :class:`~atlas_doc_parser.model.NodeRule`
    - :class:`~atlas_doc_parser.model.NodeStatus`
    - :class:`~atlas_doc_parser.model.NodeTable`
    - :class:`~atlas_doc_parser.model.NodeTableCell`
    - :class:`~atlas_doc_parser.model.NodeTableHeader`
    - :class:`~atlas_doc_parser.model.NodeTableRow`
    - :class:`~atlas_doc_parser.model.NodeTaskItem`
    - :class:`~atlas_doc_parser.model.NodeTaskList`
    - :class:`~atlas_doc_parser.model.NodeText`
