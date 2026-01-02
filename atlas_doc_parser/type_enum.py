# -*- coding: utf-8 -*-

"""
Atlassian Document Format (ADF) type enumeration.

This module defines the ``TypeEnum`` enum containing all valid ``type`` field values
for ADF nodes and marks.

Reference:

- ADF Structure: https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
- Full JSON Schema: https://unpkg.com/@atlaskit/adf-schema@51.5.4/dist/json-schema/v1/full.json
"""

import enum


class TypeEnum(enum.Enum):
    """
    Enumeration of all valid ``type`` field values in Atlassian Document Format (ADF).

    ADF is a rich text format used in Confluence pages and Jira issue fields.
    Each ADF element (node or mark) has a ``type`` field that identifies its kind.

    **Marks** (inline formatting applied to text nodes):

    - ``alignment`` - Text alignment (left, center, right)
    - ``annotation`` - Inline comments/annotations
    - ``backgroundColor`` - Background color highlighting
    - ``border`` - Border styling
    - ``breakout`` - Layout breakout mode
    - ``code`` - Inline code formatting (monospace)
    - ``em`` - Emphasis (italic text)
    - ``indentation`` - Text indentation level
    - ``link`` - Hyperlink
    - ``strike`` - Strikethrough text
    - ``strong`` - Strong emphasis (bold text)
    - ``subsup`` - Subscript or superscript text
    - ``textColor`` - Text color
    - ``underline`` - Underlined text

    **Nodes** (structural elements that form the document tree):

    - ``doc`` - Root document node
    - ``text`` - Plain text content (leaf node)
    - ``paragraph`` - Paragraph block
    - ``heading`` - Heading (h1-h6)
    - ``bulletList`` - Unordered list
    - ``orderedList`` - Ordered (numbered) list
    - ``listItem`` - List item within bullet/ordered list
    - ``blockquote`` - Block quotation
    - ``codeBlock`` - Code block with syntax highlighting
    - ``table`` - Table container
    - ``tableRow`` - Table row
    - ``tableCell`` - Table data cell
    - ``tableHeader`` - Table header cell
    - ``panel`` - Info/warning/error/note panel
    - ``rule`` - Horizontal rule (divider)
    - ``hardBreak`` - Hard line break
    - ``mention`` - User/team mention
    - ``emoji`` - Emoji character
    - ``date`` - Date picker value
    - ``status`` - Status lozenge
    - ``media`` - Media file (image/video/file)
    - ``mediaGroup`` - Group of media items
    - ``mediaSingle`` - Single media item with layout
    - ``mediaInline`` - Inline media
    - ``inlineCard`` - Inline smart link card
    - ``blockCard`` - Block smart link card
    - ``embedCard`` - Embedded content card
    - ``expand`` - Expandable/collapsible section
    - ``nestedExpand`` - Nested expandable section
    - ``layoutSection`` - Multi-column layout container
    - ``layoutColumn`` - Column within layout section
    - ``taskList`` - Task/checkbox list
    - ``taskItem`` - Task/checkbox item
    - ``decisionList`` - Decision list
    - ``decisionItem`` - Decision item
    - ``extension`` - App extension (block-level)
    - ``inlineExtension`` - App extension (inline)
    - ``bodiedExtension`` - App extension with body content
    - ``placeholder`` - Placeholder text
    - ``caption`` - Media caption

    Reference:
        - ADF Structure: https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/
        - JSON Schema: https://unpkg.com/@atlaskit/adf-schema@51.5.4/dist/json-schema/v1/full.json
    """

    # Marks (inline formatting)
    alignment = "alignment"
    annotation = "annotation"
    backgroundColor = "backgroundColor"
    border = "border"
    breakout = "breakout"
    code = "code"
    em = "em"
    indentation = "indentation"
    link = "link"
    strike = "strike"
    strong = "strong"
    subsup = "subsup"
    textColor = "textColor"
    underline = "underline"

    # Nodes (structural elements)
    blockCard = "blockCard"
    blockTaskItem = "blockTaskItem"
    blockquote = "blockquote"
    bodiedExtension = "bodiedExtension"
    bodiedSyncBlock = "bodiedSyncBlock"
    bulletList = "bulletList"
    caption = "caption"
    codeBlock = "codeBlock"
    dataConsumer = "dataConsumer"
    date = "date"
    decisionItem = "decisionItem"
    decisionList = "decisionList"
    doc = "doc"
    embedCard = "embedCard"
    emoji = "emoji"
    expand = "expand"
    extension = "extension"
    external = "external"
    file = "file"
    fragment = "fragment"
    hardBreak = "hardBreak"
    heading = "heading"
    image = "image"
    inlineCard = "inlineCard"
    inlineExtension = "inlineExtension"
    layoutColumn = "layoutColumn"
    layoutSection = "layoutSection"
    listItem = "listItem"
    media = "media"
    mediaGroup = "mediaGroup"
    mediaInline = "mediaInline"
    mediaSingle = "mediaSingle"
    mention = "mention"
    nestedExpand = "nestedExpand"
    orderedList = "orderedList"
    panel = "panel"
    paragraph = "paragraph"
    placeholder = "placeholder"
    rule = "rule"
    status = "status"
    sub = "sub"
    sup = "sup"
    syncBlock = "syncBlock"
    table = "table"
    tableCell = "tableCell"
    tableHeader = "tableHeader"
    tableRow = "tableRow"
    taskItem = "taskItem"
    taskList = "taskList"
    text = "text"


def check_type_match(
    type_value: str,
    expected_types: TypeEnum | list[TypeEnum],
) -> bool:
    """
    Check if a type string matches one or more expected TypeEnum values.

    This helper function is used to validate ADF element types during parsing.
    It compares a raw type string from JSON against expected TypeEnum member(s).

    :param type_value: The raw ``type`` field value from ADF JSON (e.g., "paragraph", "text").
    :param expected_types: A single TypeEnum member or list of TypeEnum members
        to match against. If a list is provided, returns True if type_value
        matches ANY of the expected types.

    :return: True if type_value matches (any of) the expected type(s), False otherwise.

    Example::

        >>> check_type_match("paragraph", TypeEnum.paragraph)
        True
        >>> check_type_match("text", [TypeEnum.paragraph, TypeEnum.text])
        True
        >>> check_type_match("heading", TypeEnum.paragraph)
        False
    """
    if not isinstance(expected_types, list):
        expected_types = [expected_types]
    expected_values = [t.value for t in expected_types]
    return type_value in expected_values