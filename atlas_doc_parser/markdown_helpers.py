# -*- coding: utf-8 -*-

"""
Markdown Conversion Helper Functions for ADF

This module provides utility functions to convert Atlassian Document Format (ADF)
nodes and marks into Markdown text. These helpers are used by the mixin classes
to implement the ``to_markdown()`` method for each ADF element.

Key concepts:

- ADF documents have a tree structure with nodes (paragraph, heading, etc.)
  and marks (bold, italic, link, etc.)
- Marks modify how text is displayed (e.g., bold wraps text with ``**``)
- Content nodes can contain child nodes that need recursive conversion
"""

import typing as T

from func_args.api import OPT

from .type_enum import TypeEnum

if T.TYPE_CHECKING:  # pragma: no cover
    from .mark_or_node import T_MARK, T_NODE


def strip_double_empty_line(
    text: str,
    n: int = 3,
) -> str:
    """
    Remove excessive consecutive empty lines from text.

    In Markdown, multiple blank lines are typically rendered the same as
    a single blank line. This function normalizes the output by replacing
    three or more consecutive newlines with exactly two (one blank line).

    Args:
        text: The input text that may contain excessive blank lines.
        n: Number of replacement iterations to perform. Default is 3,
           which handles up to 5 consecutive newlines being reduced to 2.

    Returns:
        Text with at most one consecutive blank line (two newlines).

    Example:
        >>> strip_double_empty_line("Hello\\n\\n\\n\\nWorld")
        'Hello\\n\\nWorld'
    """
    for _ in range(n):
        text = text.replace("\n\n\n", "\n\n")
    return text


def content_to_markdown(
    content: T.Union[list["T_NODE"], T.Literal[OPT]],
    concat: str = "",
    ignore_error: bool = False,
) -> str:
    """
    Convert a list of child nodes to concatenated Markdown text.

    This function is used for **inline content** where child nodes should be
    joined without separators. For example, a paragraph containing multiple
    text nodes with different marks should be concatenated directly.

    Args:
        content: List of child nodes to convert. If ``OPT`` (not provided),
            returns an empty string.
        concat: String to join the converted markdown of each node.
            Default is empty string for inline concatenation.
        ignore_error: If True, silently skip nodes that fail to convert.
            If False (default), propagate exceptions.

    Returns:
        Concatenated Markdown text from all child nodes.

    Example:
        For a paragraph with content ``[TextNode("Hello "), TextNode("world")]``:

        >>> content_to_markdown(paragraph.content)
        'Hello world'
    """
    if content is OPT:
        return ""
    else:
        lst = list()
        for node in content:
            try:
                md = node.to_markdown()
                lst.append(md)
            except Exception as e:  # pragma: no cover
                if ignore_error:
                    pass
                else:
                    raise e
        return concat.join(lst)


def doc_content_to_markdown(
    content: T.Union[list["T_NODE"], T.Literal[OPT]],
    concat: str = "\n",
    ignore_error: bool = False,
) -> str:
    """
    Convert document-level (whole confluence page) block content to Markdown text.

    This function is used for **block-level content** where each child node
    represents a separate block (paragraph, heading, list, etc.). Unlike
    :func:`content_to_markdown`, this function:

    1. Joins blocks with newlines (default separator)
    2. Adds extra padding around certain block types (lists, code blocks)
       to ensure proper Markdown rendering
    3. Cleans up excessive blank lines in the final output

    The extra padding is needed because some Markdown renderers require
    blank lines before/after lists and code blocks to render them correctly.

    Args:
        content: List of block-level child nodes. If ``OPT``, returns empty string.
        concat: String to join blocks. Default is newline for block separation.
        ignore_error: If True, silently skip nodes that fail to convert.

    Returns:
        Markdown text with proper block separation.

    Example:
        For a doc with ``[Paragraph, BulletList, Paragraph]``:

        >>> doc_content_to_markdown(doc.content)
        'First paragraph\\n\\n- item 1\\n- item 2\\n\\nSecond paragraph'
    """
    if content is OPT:
        return ""
    else:
        lst = list()
        for node in content:
            # print("----- Work on a new node -----")  # for debug only
            try:
                # Add extra newlines around block elements that need separation
                if node.is_type_of(
                    [
                        TypeEnum.bulletList,
                        TypeEnum.orderedList,
                        TypeEnum.codeBlock,
                    ]
                ):
                    md = "\n" + node.to_markdown() + "\n"
                else:
                    md = node.to_markdown()
                # print(f"{node = }")  # for debug only
                # print(f"{md = }")  # for debug only
                lst.append(md)
            except Exception as e:  # pragma: no cover
                if ignore_error:
                    pass
                else:
                    raise e

    md = strip_double_empty_line(concat.join(lst))
    return md


def add_style_to_markdown(
    md: str,
    node: "T_NODE",
) -> str:
    """
    Apply mark styles to Markdown text.

    In ADF, marks represent text formatting like bold, italic, links, etc.
    A node can have multiple marks that should be applied in sequence.
    Each mark's ``to_markdown()`` method wraps the text with appropriate
    Markdown syntax.

    The order of mark application matters for nested formatting:
    - Input: "text" with marks [strong, em]
    - After strong: "**text**"
    - After em: "*\\*\\*text\\*\\**"

    Args:
        md: The base Markdown text to style.
        node: The ADF node containing marks to apply. If ``node.marks`` is
            not a list, the text is returned unchanged.

    Returns:
        Markdown text with all mark styles applied.

    Example:
        For a text node "hello" with marks ``[MarkStrong, MarkEm]``:

        >>> add_style_to_markdown("hello", text_node)
        '*\\*\\*hello\\*\\**'
    """
    try:
        if isinstance(node.marks, list):
            for mark in node.marks:
                md = mark.to_markdown(md)
    # some node doesn't have marks attribute (don't support styles)
    except AttributeError:
        pass
    return md


ATLASSIAN_LANG_TO_MARKDOWN_LANG_MAPPING = {}
