# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_list_item import NodeListItem


@dataclasses.dataclass(frozen=True)
class NodeBulletList(BaseNode):
    """
    A container for an unordered (bulleted) list.

    The bulletList node is a top-level block node that groups multiple
    listItem nodes together for rendering as a bulleted list.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/bulletList/
    """

    type: str = TypeEnum.bulletList.value
    content: list["NodeListItem"] = REQ

    def to_markdown(
        self,
        level: int = 0,
        ignore_error: bool = False,
    ) -> str:
        """
        Convert the bullet list to Markdown format.

        **ADF Structure** (nested list is a **child** of listItem)::

            bulletList
            ├── listItem (item 1)
            │   ├── paragraph → text nodes    ← text wrapped in paragraph
            │   └── bulletList (nested)       ← nested list is CHILD of listItem
            │       └── listItem (item 1.1)
            │           ├── paragraph
            │           └── bulletList (nested)
            ├── listItem (item 2)
            │   ├── paragraph
            │   └── bulletList (nested)
            ...

        **Implementation**: Uses two nested loops because:

        - Outer loop: iterates over ``listItem`` nodes in ``bulletList.content``
        - Inner loop: iterates over ``listItem.content`` which contains both
          ``paragraph`` (text) and nested ``bulletList`` nodes

        .. note::

            This structure differs from :meth:`~atlas_doc_parser.nodes.node_task_list.NodeTaskList.to_markdown`
            where nested ``taskList`` nodes are **siblings** of ``taskItem`` nodes,
            not children. See :class:`~atlas_doc_parser.nodes.node_task_list.NodeTaskList` for comparison.

        .. seealso::

            - :meth:`~atlas_doc_parser.nodes.node_ordered_list.NodeOrderedList.to_markdown` - same structure, uses numbers
            - :meth:`~atlas_doc_parser.nodes.node_task_list.NodeTaskList.to_markdown` - different structure, single loop
        """
        lines = []
        indent = "    " * level  # 4 spaces per level

        for item in self.content:
            if self.is_type_of(item, TypeEnum.listItem):
                # Process the list item content
                content_lines = []
                for node in item.content:
                    if self.is_type_of(node, TypeEnum.bulletList):
                        # Nested list - increase level
                        try:
                            md = node.to_markdown(level=level + 1)
                            content_lines.append(md)
                        except Exception as e:
                            if ignore_error:
                                pass
                            else:
                                raise e
                    else:
                        # Regular content (like paragraph)
                        try:
                            md = node.to_markdown().rstrip()
                            content_lines.append(md)
                        except Exception as e:
                            if ignore_error:
                                pass
                            else:
                                raise e

                # Join the content lines
                item_content = "\n".join(content_lines)

                # Format the first line with bullet point
                bullet_content = item_content.split("\n")[0]
                first_line = f"{indent}- {bullet_content}"
                lines.append(first_line)

                # Add remaining lines
                remaining_lines = item_content.split("\n")[1:]
                if remaining_lines:
                    lines.extend(remaining_lines)

        return "\n".join(lines)
