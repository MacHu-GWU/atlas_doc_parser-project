Implementation Strategy
==============================================================================
There are two technical approaches for implementing ADF node classes:

**Approach 1: Documentation-Driven**

Use the `official ADF documentation <https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/>`_ as the source of truth. Manually read the documentation for each node type, reverse-engineer the data model from documented key-value pairs, and implement the corresponding Python dataclass. This approach is straightforward but requires manual effort for each node type.

**Approach 2: Schema-Driven**

Use the `ADF JSON Schema <https://unpkg.com/@atlaskit/adf-schema@51.5.4/dist/json-schema/v1/full.json>`_ as the source of truth. Parse the schema file programmatically and dynamically generate all Python dataclasses. This approach is more elegant and scalable, as adding new node types becomes automatic once the code generator is built.

**Trade-offs and Decision**

The schema-driven approach appears more elegant but carries significant risk. It relies on a critical assumption: the JSON Schema must be 100% consistent with the actual API behavior. Atlassian has historically had discrepancies between their published specifications and actual API implementations, causing generated clients to fail in production.

Due to this reliability concern, this project currently adopts the **documentation-driven approach**. While more labor-intensive, it provides better control and allows manual verification against real API responses. A future investigation may evaluate whether the current JSON Schema has matured to the point where schema-driven generation becomes viable.
