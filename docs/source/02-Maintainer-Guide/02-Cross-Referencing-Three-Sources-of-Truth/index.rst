Cross-Referencing Three Sources of Truth
==============================================================================
This document explains how we implement ADF node and mark dataclasses, including the information sources we use and the decision-making process.


Core Objective
------------------------------------------------------------------------------
The essence of this project is simple: **create a Python dataclass for each ADF model** such that:

1. ``from_dict()`` correctly deserializes ADF JSON into Python objects
2. ``to_dict()`` correctly serializes back to ADF JSON (round-trip)
3. ``to_markdown()`` converts the parsed structure to Markdown

The ``from_dict()`` method is the most critical - it's the foundation that enables all downstream functionality. If parsing doesn't work correctly, nothing else matters.


Information Sources
------------------------------------------------------------------------------
When implementing an ADF model, we have three potential sources of information:


Source 1: ADF JSON Schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The `ADF JSON Schema <https://unpkg.com/@atlaskit/adf-schema@51.5.4/dist/json-schema/v1/full.json>`_ provides formal definitions for all node and mark types.

**Advantages:**

- Machine-readable and precise
- Covers all known types
- Defines required vs optional fields

**Limitations:**

- May not reflect actual API behavior
- Some edge cases are not documented
- Schema versions may lag behind production


Source 2: Official Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The `official ADF documentation <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>`_ provides human-readable descriptions.

**Advantages:**

- Explains purpose and usage
- Provides simple examples
- Official reference from Atlassian

**Limitations:**

- Often incomplete or minimal
- May be outdated
- Examples may not cover all attributes


.. _source3-real-confluence-pages:

Source 3: Real Confluence Pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Actual ADF JSON extracted from real Confluence pages shows how the format is used in practice.

**Advantages:**

- Ground truth - this is what the API actually returns
- Reveals undocumented attributes
- Shows real-world usage patterns

**Limitations:**

- Requires manual creation of test pages
- May miss rarely-used features
- Specific to your Confluence instance

We maintain a dedicated Confluence folder for test pages:

- `atlas_doc_parser-project Test Pages <https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082092/atlas_doc_parser-project>`_

This folder contains sample pages for each ADF node and mark type, used for extracting real-world ADF JSON examples.


.. _tracking-the-three-sources:

Tracking the Three Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
We maintain a Google Sheet that tracks the relationship between all three sources for each ADF type:

- `atlas_doc_parser Google Sheet <https://docs.google.com/spreadsheets/d/1ETVEHWFAP-ugkIgZebLrmUF8pZ0EY6OHpyXlhdkLdwc/edit?gid=0#gid=0>`_

This spreadsheet serves as the master reference for implementation, mapping:

1. **JSON Schema definition name** (e.g., ``codeBlock_node``)
2. **Official documentation URL** (if available)
3. **Test Confluence page URL** (for real-world examples)
4. **Implementation status** (implemented, in progress, not started)

When starting to implement a new ADF type, always consult this spreadsheet first to understand what resources are available.


The Cross-Reference Approach
------------------------------------------------------------------------------
**No single source can be blindly trusted.**

Atlassian has historically had discrepancies between:

- Published JSON schemas and actual API behavior
- Official documentation and real implementations
- Different versions of their products

Therefore, we follow a **cross-reference approach**:

1. **Start with the JSON Schema** - Get the formal definition of a model
2. **Check official documentation** - Understand the intended purpose and usage
3. **Verify with real examples** - Extract actual ADF from Confluence pages

When sources disagree:

- Real Confluence page output is the **ultimate source of truth**
- The JSON schema is the **primary reference**
- Official documentation provides **context and intent**

If discrepancies are significant, document them and make a pragmatic decision based on what actually works.


Implementation Workflow
------------------------------------------------------------------------------


Step 1: Identify the Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Each ADF type corresponds to:

- A **definition** in the JSON schema (e.g., ``codeBlock_node``, ``strong_mark``)
- A **Python module** (e.g., ``node_code_block.py``, ``mark_strong.py``)
- A **Python class** (e.g., ``NodeCodeBlock``, ``MarkStrong``)

Note: In some cases, multiple schema definitions may map to a single Python class (e.g., different variants of a node).


Step 2: Gather Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Query the JSON schema for the definition (use `adf-format-json-schema` agent skill)
2. Fetch official documentation (if available)
3. Create a test Confluence page with the element
4. Extract the ADF JSON from that page (use `adf-json-example` agent skill)


Step 3: Cross-Reference and Validate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Compare all sources:

- Do the schema fields match the real JSON?
- Are there undocumented attributes in the real example?
- Does the official documentation describe all fields?

Resolve discrepancies by prioritizing real behavior over documented behavior.


Step 4: Implement the Dataclass
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create the Python dataclass following these rules:

- Use ``REQ`` for required fields, ``OPT`` for optional fields
- Use ``TypeEnum.xxx.value`` for the ``type`` field
- Use cross-reference type hints for nested nodes/marks
- Do not use ``T.Optional`` (the ``OPT`` sentinel already indicates optionality)


Step 5: Register the Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Add the new class to the type mapping:

- Nodes: ``NODE_TYPE_TO_CLASS_MAPPING`` in ``parse_node.py``
- Marks: ``MARK_TYPE_TO_CLASS_MAPPING`` in ``parse_mark.py``


Step 6: Write Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create tests that verify:

- ``from_dict()`` correctly parses the real ADF example
- ``to_dict()`` produces equivalent output (round-trip)
- ``to_markdown()`` produces expected Markdown output


Why This Approach?
------------------------------------------------------------------------------
We chose this pragmatic, verification-based approach because:

1. **Reliability over elegance**: A fully automated schema-driven generator sounds nice, but breaks when schemas don't match reality.
2. **Incremental progress**: We can implement models one at a time, testing each thoroughly before moving on.
3. **Real-world validation**: Every model is verified against actual Confluence/Jira output, not just specifications.
4. **Graceful degradation**: Unimplemented types are skipped rather than causing failures (see :doc:`../06-Graceful-Handling-of-Unimplemented-Types/index`).

The result is a library that may not cover 100% of ADF types immediately, but what it does cover works reliably in production.
