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

    During ``to_markdown()`` conversion, many block-level nodes automatically
    add blank lines before/after themselves to ensure proper separation from
    surrounding content. This can result in 3 or more consecutive blank lines
    when multiple blocks are adjacent, which looks ugly in the final output.

    This function normalizes the output by collapsing excessive blank lines
    (3+ newlines) down to exactly one blank line (2 newlines).

    :param text: The input text that may contain excessive blank lines.
    :param n: Number of replacement iterations to perform. Default is 3,
        which handles up to 5 consecutive newlines being reduced to 2.
    :return: Text with at most one consecutive blank line (two newlines).

    Example::

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
    Recursively convert a node's content (child nodes) to Markdown text.

    This is the core recursive function for ``to_markdown()`` conversion.
    It iterates through all child nodes in the ``content`` list, calls
    ``to_markdown()`` on each, and concatenates the results.

    This function is used for **inline content** where child nodes should be
    joined without separators. For example, a paragraph containing multiple
    text nodes with different formatting should be concatenated directly.

    :param content: List of child nodes to convert. If ``OPT`` (not provided),
        returns an empty string.
    :param concat: String to join the converted markdown of each node.
        Default is empty string for inline concatenation.
    :param ignore_error: If True, silently skip nodes that fail to convert.
        If False (default), propagate exceptions. This flag is passed down
        to nested ``to_markdown()`` calls.
    :return: Concatenated Markdown text from all child nodes.

    Example::

        # In NodeParagraph.to_markdown():
        md = content_to_markdown(self.content, ignore_error=ignore_error)
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
    Convert document-level (whole Confluence page) content to Markdown text.

    This function is specifically for the ``NodeDoc`` root node - the entire
    page level. It differs from :func:`content_to_markdown` in that it handles
    **block-level content** with additional processing:

    1. Joins blocks with newlines (not empty string)
    2. Adds extra blank lines around lists and code blocks for proper rendering
    3. Cleans up excessive blank lines using :func:`strip_double_empty_line`

    The extra padding around lists and code blocks is needed because some
    Markdown renderers require blank lines before/after these elements to
    render them correctly as separate blocks.

    :param content: List of block-level child nodes (paragraphs, headings,
        lists, tables, etc.). If ``OPT``, returns empty string.
    :param concat: String to join blocks. Default is newline for block separation.
    :param ignore_error: If True, silently skip nodes that fail to convert.
    :return: Markdown text with proper block separation.

    Example::

        # In NodeDoc.to_markdown():
        return doc_content_to_markdown(self.content, ignore_error=ignore_error)
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
    Apply a node's marks (formatting) to Markdown text.

    This function handles the ``marks`` field of a node. In ADF, marks represent
    text formatting like bold, italic, links, text color, etc. A node can have
    multiple marks that should be applied in sequence.

    Each mark's ``to_markdown(text)`` method wraps the text with appropriate
    Markdown syntax (e.g., ``**text**`` for bold, ``*text*`` for italic).

    :param md: The base Markdown text to apply formatting to.
    :param node: The ADF node containing marks to apply. If ``node.marks`` is
        not a list (e.g., the node doesn't support marks), the text is returned
        unchanged.
    :return: Markdown text with all mark styles applied.

    Example::

        # In NodeText.to_markdown():
        md = self.text
        md = add_style_to_markdown(md, self)
        return md
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
