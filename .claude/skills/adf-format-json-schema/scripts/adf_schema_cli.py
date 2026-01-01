# -*- coding: utf-8 -*-

"""
ADF JSON Schema CLI Tool

This command-line tool queries the Atlassian Document Format (ADF) JSON schema
to help developers understand the structure of ADF nodes and marks when
implementing them as Python dataclasses.

The schema is sourced from the @atlaskit/adf-schema npm package and contains
definitions for all node types (paragraph, heading, table, etc.) and mark types
(strong, em, link, etc.) used in Confluence and Jira.

Usage:
    # List all available definitions with their properties
    python adf_schema_cli.py list_def

    # Get the full JSON schema for a specific definition
    python adf_schema_cli.py get_def <definition_name>

Examples:
    python adf_schema_cli.py list_def
    python adf_schema_cli.py get_def paragraph_node
    python adf_schema_cli.py get_def strong_mark
"""

import json

import fire

from atlas_doc_parser.tests.data.schema import adf_json_schema


class Command:
    """
    CLI command class for querying ADF JSON schema definitions.

    This class provides two main operations:
    - list_def: List all definition names and their top-level properties
    - get_def: Get the complete JSON schema for a specific definition
    """

    def list_def(self) -> None:
        """
        List all definitions in the ADF JSON schema.

        Prints each definition name along with its top-level properties,
        sorted alphabetically by definition name.

        Output format:
            name = <definition_name>, properties = [<property_list>]

        Definition naming conventions:
            - *_node: Node types (e.g., paragraph_node, heading_node)
            - *_mark: Mark types (e.g., strong_mark, em_mark)
        """
        defs = list(adf_json_schema.data["definitions"])
        defs.sort()
        for def_name in defs:
            def_value = adf_json_schema.data["definitions"][def_name]
            properties = list(def_value.get("properties", {}))
            print(f"name = {def_name}, properties = {properties}")

    def get_def(self, def_name: str) -> None:
        """
        Get the complete JSON schema for a specific definition.

        Args:
            def_name: The name of the definition to retrieve
                      (e.g., 'paragraph_node', 'strong_mark')

        Prints the definition as formatted JSON, including:
            - type: The JSON Schema type (usually 'object')
            - properties: Property definitions with types and constraints
            - required: List of required properties
            - additionalProperties: Whether extra properties are allowed
        """
        def_value = adf_json_schema.data["definitions"][def_name]
        print(json.dumps(def_value, indent=2))


if __name__ == "__main__":
    fire.Fire(Command)
