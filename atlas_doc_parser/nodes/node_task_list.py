# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode


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
    content: T.List[BaseNode] = OPT

    def to_markdown(
        self,
        level: int = 0,
        ignore_error: bool = False,
    ) -> str:
        lines = []
        indent = "    " * level  # 4 spaces per level

        for item in self.content:
            if self.is_type_of(item, TypeEnum.taskItem):
                # Process the list item content
                content_lines = []
                for node in item.content:
                    if self.is_type_of(node, TypeEnum.taskList):
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
                first_line = f"{indent}- [ ] {bullet_content}"
                lines.append(first_line)

                # Add remaining lines
                remaining_lines = item_content.split("\n")[1:]
                if remaining_lines:
                    lines.extend(remaining_lines)

        return "\n".join(lines)
