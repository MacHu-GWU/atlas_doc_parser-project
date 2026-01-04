Implementation Strategy
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

1. Query the JSON schema for the definition
2. Fetch official documentation (if available)
3. Create a test Confluence page with the element
4. Extract the ADF JSON from that page

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

4. **Graceful degradation**: Unimplemented types are skipped rather than causing failures (see :doc:`../graceful-handling-of-unimplemented-types`).

The result is a library that may not cover 100% of ADF types immediately, but what it does cover works reliably in production.
