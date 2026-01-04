How to Test Marks and Nodes
==============================================================================
This document explains how to write tests for ADF mark and node implementations. After implementing a dataclass following :ref:`implementing-a-new-mark-or-node-class`, testing is the next step.


Testing Infrastructure Overview
------------------------------------------------------------------------------
The testing framework has a two-layer architecture:

1. **PageSample**: Represents a Confluence page with cached ADF content
2. **AdfSample**: Extracts a specific node/mark from a PageSample via JMESPath

This design allows multiple samples to be extracted from the same page (e.g., both ``mark_sub`` and ``mark_sup`` from a single "subsup" page).


Step 1: Create a Test Confluence Page
------------------------------------------------------------------------------
Create a test page in the :ref:`source3-real-confluence-pages` folder that contains the mark or node element you want to test.

For example, to test the ``strong`` mark:

1. Go to the `atlas_doc_parser-project Test Pages <https://sanhehu.atlassian.net/wiki/spaces/GitHubMacHuGWU/pages/654082092/atlas_doc_parser-project>`_ folder
2. Create a new page named ``Mark - strong``
3. Add content that includes the ``strong`` mark (bold text)

This page will serve as the source of real ADF JSON for testing.


Step 2: Register the Sample in AdfSampleEnum
------------------------------------------------------------------------------
Open :mod:`atlas_doc_parser.tests.data.samples` and add entries to the ``AdfSampleEnum`` class.


Basic Pattern - Single Sample per Page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For simple cases where one page tests one element:

.. code-block:: python

    node_text = PageSample(
        name="node_text",  # Cache filename (saved as {name}.json)
        url="https://sanhehu.atlassian.net/wiki/spaces/.../pages/.../Node+-+text",
    ).get_sample(
        jpath="content[0].content[0]",  # JMESPath to locate the target element
        md="this is a text.",  # Expected markdown output
    )


Multiple Samples from One Page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When a single page contains multiple elements to test, use the ``_page`` pattern:

.. code-block:: python

    # First, create the PageSample
    _page = PageSample(
        name="mark_subsup",
        url="https://sanhehu.atlassian.net/wiki/spaces/.../Mark+-+subsup",
    )

    # Then extract multiple samples from it
    mark_sub = _page.get_sample(jpath="content[0].content[1].marks[1]")
    mark_sup = _page.get_sample(jpath="content[0].content[3].marks[1]")
    node_sub_text = _page.get_sample(
        jpath="content[0].content[1]",
        md="sub",
    )
    node_sup_text = _page.get_sample(
        jpath="content[0].content[3]",
        md="sup",
    )


Debugging: Finding the Right JPath
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
During development, you may not know the exact JMESPath to locate your target element. Use this debugging workflow:

1. **Set ``md`` to any value or ``None``** - The test will fail, but you'll see the ADF JSON structure
2. **Run the test** - The printed ADF JSON shows you the structure
3. **Adjust ``jpath``** to locate the correct element
4. **Update ``md``** to the expected Markdown output

.. code-block:: python

    # During debugging - let it fail to see the structure
    node_my_element = PageSample(
        name="node_my_element",
        url="https://...",
    ).get_sample(
        jpath="content[0]",  # Adjust this based on what you see
        md=None,  # Set to None or any placeholder during debugging
    )


PageSample Class Methods
------------------------------------------------------------------------------


adf_no_cache Property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fetches ADF content directly from the Confluence API without using cache:

.. code-block:: python

    page = PageSample(name="...", url="...")
    data = page.adf_no_cache  # Always fetches from API

Use this when:

- You've updated the Confluence page and need fresh data
- You're debugging API connectivity issues
- You want to verify the cache is correct


adf Property
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fetches ADF content with caching enabled:

.. code-block:: python

    page = PageSample(name="...", url="...")
    data = page.adf  # Loads from cache if available, otherwise fetches and caches

**Cache behavior:**

1. Checks if ``{test_pages_dir}/{name}.json`` exists
2. If exists, loads and returns the cached JSON
3. If not, fetches from API, saves to cache file, and returns the data

Use this for normal test runs - it avoids repeated API calls.


get_sample Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Creates an ``AdfSample`` that extracts a specific node/mark from the page:

.. code-block:: python

    page = PageSample(name="...", url="...")
    sample = page.get_sample(
        jpath="content[0].content[1].marks[0]",  # JMESPath expression
        md="expected markdown",  # Optional expected output
    )


AdfSample Class Methods
------------------------------------------------------------------------------


get_inst Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Deserializes the extracted ADF JSON into a Python dataclass instance:

.. code-block:: python

    sample = AdfSampleEnum.mark_strong
    mark = sample.get_inst(MarkStrong)
    # mark is now a MarkStrong instance

Use this when you need the deserialized instance for further operations but don't want to run full tests.


test_node_or_mark Static Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A low-level test helper that tests serialization/deserialization and optionally Markdown conversion:

.. code-block:: python

    # Create instance manually
    node = NodeText.from_dict({"type": "text", "text": "Hello"})

    # Test it
    AdfSample.test_node_or_mark(node, markdown="Hello")

This method:

1. Calls ``check_seder()`` - verifies round-trip serialization
2. If instance is a ``BaseNode`` and ``markdown`` is provided, calls ``check_markdown()`` to verify Markdown output

Use this when you have manually created test data instead of Confluence page data.


test Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The main test method that combines everything:

.. code-block:: python

    sample = AdfSampleEnum.node_text
    node = sample.test(NodeText)

This method:

1. Prints the raw ADF JSON for debugging
2. Deserializes the JSON using ``klass.from_dict()``
3. Tests serialization/deserialization round-trip
4. Tests Markdown output if ``md`` was specified in ``get_sample()``
5. Returns the deserialized instance for additional assertions

Use this as your primary testing method.


Step 3: Write the Test File
------------------------------------------------------------------------------
Create a test file in the appropriate directory:

- **Marks**: ``tests/marks/test_marks_mark_{snake_name}.py``
- **Nodes**: ``tests/nodes/test_nodes_node_{snake_name}.py``


Basic Test Pattern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: python

    # tests/marks/test_marks_mark_strong.py
    from atlas_doc_parser.marks.mark_strong import MarkStrong
    from atlas_doc_parser.tests.data.samples import AdfSampleEnum


    class TestMarkStrong:
        def test_basic_strong_mark(self):
            mark = AdfSampleEnum.mark_strong.test(MarkStrong)

            # Additional assertions on the mark instance
            valid_text = ["Hello world", "Hello * World ** !"]
            for before in valid_text:
                assert mark.to_markdown(before) == f"**{before}**"


    if __name__ == "__main__":
        from atlas_doc_parser.tests import run_cov_test

        run_cov_test(
            __file__,
            "atlas_doc_parser.marks.mark_strong",
            preview=False,
        )


Testing with Manual Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sometimes you need to test edge cases not covered by Confluence pages:

.. code-block:: python

    # tests/nodes/test_nodes_node_text.py
    from atlas_doc_parser.nodes.node_text import NodeText
    from atlas_doc_parser.tests.data.samples import AdfSampleEnum, AdfSample


    class TestNodeText:
        def test_node_text_basic(self):
            node = AdfSampleEnum.node_text.test(NodeText)

        def test_node_text_with_titled_hyperlink(self):
            # Manual test data for edge case
            data = {
                "text": "Atlassian",
                "type": "text",
                "marks": [
                    {
                        "type": "link",
                        "attrs": {
                            "href": "http://atlassian.com",
                            "title": "Atlassian",
                        },
                    }
                ],
            }
            node = NodeText.from_dict(data)
            md = "[Atlassian](http://atlassian.com)"
            AdfSample.test_node_or_mark(node, md)


Running Tests
------------------------------------------------------------------------------


Run a Single Test File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Execute the test file directly to run with coverage:

.. code-block:: bash

    .venv/bin/python tests/marks/test_marks_mark_strong.py

This runs the test and generates a coverage report for the target module.


Run All Tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

    make test      # Run all unit tests
    make cov       # Run with coverage analysis
    make view-cov  # View coverage report in browser


Implementation Order
------------------------------------------------------------------------------
When implementing marks and nodes, follow this order:

1. **Marks first** - They have fewer dependencies (marks don't nest other marks)
2. **Simple nodes** - Nodes without nested content (e.g., ``text``, ``rule``, ``hardBreak``)
3. **Container nodes** - Nodes with content (e.g., ``paragraph``, ``heading``)
4. **Complex nodes** - Nodes with multiple nested types (e.g., ``table``, ``listItem``)

The :ref:`tracking-the-three-sources` Google Sheet is already sorted in the recommended implementation order.


Complete Workflow Summary
------------------------------------------------------------------------------
1. **Implement the dataclass** following :ref:`implementing-a-new-mark-or-node-class`
2. **Create/update Confluence test page** in :ref:`source3-real-confluence-pages`
3. **Add sample to AdfSampleEnum** with appropriate ``jpath`` and ``md``
4. **Write test file** using the ``sample.test(Klass)`` pattern
5. **Run tests** to verify implementation
6. **Move to next type** in the Google Sheet

This systematic approach ensures each mark/node is thoroughly tested with real-world data before moving on.
