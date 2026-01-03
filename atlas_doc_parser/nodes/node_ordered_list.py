# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


@dataclasses.dataclass(frozen=True)
class NodeOrderedListAttrs(Base):
    """
    Attributes for :class:`NodeOrderedList`.

    :param order: Optional. Specifies the starting number for the list.
        Accepts values >= 0. Defaults to 1 when not specified.
    :param localId: Optional. A unique identifier for the node.
    """

    order: T.Optional[int] = OPT
    localId: T.Optional[str] = OPT


@dataclasses.dataclass(frozen=True)
class NodeOrderedList(BaseNode):
    """
    A container for an ordered (numbered) list.

    The orderedList node is a top-level block node that groups multiple
    listItem nodes together for rendering as a numbered list. The ``order``
    attribute can be used to specify the starting number.

    - https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/orderedList/
    """

    type: str = TypeEnum.orderedList.value
    attrs: NodeOrderedListAttrs = OPT
    content: T.List[BaseNode] = OPT

    def to_markdown(
        self,
        level: int = 0,
        ignore_error: bool = False,
    ) -> str:
        """
        Convert the ordered list to Markdown format.

        **ADF Structure** (nested list is a **child** of listItem)::

            orderedList
            ├── listItem (item 1)
            │   ├── paragraph → text nodes    ← text wrapped in paragraph
            │   └── orderedList (nested)      ← nested list is CHILD of listItem
            │       └── listItem (item 1.1)
            │           ├── paragraph
            │           └── orderedList (nested)
            ├── listItem (item 2)
            │   ├── paragraph
            │   └── orderedList (nested)
            ...

        **Implementation**: Uses two nested loops because:

        - Outer loop: iterates over ``listItem`` nodes in ``orderedList.content``
        - Inner loop: iterates over ``listItem.content`` which contains both
          ``paragraph`` (text) and nested ``orderedList`` nodes

        .. note::

            This structure differs from :meth:`NodeTaskList.to_markdown` where
            nested ``taskList`` nodes are **siblings** of ``taskItem`` nodes,
            not children. See :class:`NodeTaskList` for comparison.

        .. seealso::

            - :meth:`NodeBulletList.to_markdown` - same structure, uses bullets
            - :meth:`NodeTaskList.to_markdown` - different structure, single loop
        """
        lines = []
        indent = "    " * level  # 4 spaces per level

        # Start numbering from attrs.order (or 1 for inner levels)
        if level == 0 and isinstance(self.attrs.order, int):
            current_num = self.attrs.order
        else:
            current_num = 1

        for item in self.content:
            if self.is_type_of(item, TypeEnum.listItem):
                # Process the list item content
                content_lines = []
                for node in item.content:
                    if self.is_type_of(node, TypeEnum.orderedList):
                        # Nested list - increase level
                        try:
                            md = node.to_markdown(level=level + 1)
                            content_lines.append(md)
                        except Exception as e:  # pragma: no cover
                            if ignore_error:
                                pass
                            else:
                                raise e
                    else:
                        # Regular content (like paragraph)
                        try:
                            md = node.to_markdown().rstrip()
                            content_lines.append(md)
                        except Exception as e:  # pragma: no cover
                            if ignore_error:
                                pass
                            else:
                                raise e

                # Join the content lines
                item_content = "\n".join(content_lines)

                # Format the first line with number
                first_content = item_content.split("\n")[0]
                first_line = f"{indent}{current_num}. {first_content}"
                lines.append(first_line)

                # Add remaining lines
                remaining_lines = item_content.split("\n")[1:]
                if remaining_lines:
                    lines.extend(remaining_lines)

                current_num += 1

        return "\n".join(lines)
