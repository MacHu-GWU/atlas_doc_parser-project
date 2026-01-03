# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_task_item import NodeTaskItem
    from .node_block_task_item import NodeBlockTaskItem


@dataclasses.dataclass(frozen=True)
class NodeTaskListAttrs(Base):
    """
    Attributes for :class:`NodeTaskList`.

    :param localId: A unique identifier for the task list.
    """

    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodeTaskList(BaseNode):
    """
    A container for task/checkbox items.

    The taskList node is a block node that groups multiple taskItem nodes
    together for rendering as a checklist. It can also contain nested
    taskList nodes for hierarchical task structures.
    """

    type: str = TypeEnum.taskList.value
    attrs: NodeTaskListAttrs = OPT
    content: list[
        T.Union[
            "NodeTaskItem",
            "NodeTaskList",
            "NodeBlockTaskItem",
        ]
    ] = OPT

    def to_markdown(
        self,
        level: int = 0,
        ignore_error: bool = False,
    ) -> str:
        """
        Convert the task list to Markdown format.

        **ADF Structure** (nested list is a **sibling** of taskItem)::

            taskList
            ├── taskItem (item 1) → [text nodes]  ← text directly in content
            ├── taskList (nested)                  ← nested list is SIBLING of taskItem
            │   ├── taskItem (item 1.1)
            │   └── taskList (nested)
            │       └── taskItem (item 1.1.1)
            ├── taskItem (item 2)
            ├── taskList (nested)
            ...

        **Implementation**: Uses a single loop because:

        - ``taskItem`` and nested ``taskList`` are **siblings** in ``taskList.content``
        - Text nodes are directly inside ``taskItem.content`` (no wrapper like paragraph)
        - The loop handles both ``taskItem`` (render with checkbox) and
          ``taskList`` (recursive call with increased level) in the same iteration

        .. note::

            This structure differs from :meth:`~atlas_doc_parser.nodes.node_bullet_list.NodeBulletList.to_markdown`
            and :meth:`~atlas_doc_parser.nodes.node_ordered_list.NodeOrderedList.to_markdown`
            where nested lists are **children** of ``listItem`` nodes, requiring two nested loops.

        .. seealso::

            - :meth:`~atlas_doc_parser.nodes.node_bullet_list.NodeBulletList.to_markdown` - different structure, two loops
            - :meth:`~atlas_doc_parser.nodes.node_ordered_list.NodeOrderedList.to_markdown` - different structure, two loops
        """
        lines = []
        indent = "    " * level  # 4 spaces per level

        for item in self.content:
            if self.is_type_of(item, TypeEnum.taskItem):
                # Process the task item content (text nodes)
                content_parts = []
                for node in item.content:
                    try:
                        md = node.to_markdown()
                        content_parts.append(md)
                    except Exception as e:
                        if ignore_error:
                            pass
                        else:
                            raise e

                # Join content parts (they should be on the same line)
                # Use rstrip() on the final result to remove trailing whitespace
                item_content = "".join(content_parts).rstrip()

                # Determine checkbox state based on item.attrs.state
                checkbox = "[x]" if item.attrs.state == "DONE" else "[ ]"

                # Format the line with checkbox
                line = f"{indent}- {checkbox} {item_content}"
                lines.append(line)

            elif self.is_type_of(item, TypeEnum.taskList):
                # Nested task list - increase level
                try:
                    md = item.to_markdown(level=level + 1, ignore_error=ignore_error)
                    lines.append(md)
                except Exception as e:
                    if ignore_error:
                        pass
                    else:
                        raise e

        return "\n".join(lines)
