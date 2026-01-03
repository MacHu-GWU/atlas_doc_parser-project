# -*- coding: utf-8 -*-

import typing as T
import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import content_to_markdown


@dataclasses.dataclass(frozen=True)
class NodeTaskItemAttrs(Base):
    """
    Attributes for :class:`NodeTaskItem`.

    :param localId: A unique identifier for the task item.
    :param state: The state of the task item. Either "TODO" or "DONE".
    """

    localId: str = OPT
    state: T.Literal["TODO", "DONE"] = OPT


@dataclasses.dataclass(frozen=True)
class NodeTaskItem(BaseNode):
    """
    A single task/checkbox item within a taskList.

    The taskItem node represents a checkable item in a task list. Each task
    item has a unique localId and a state indicating whether the task is
    complete ("DONE") or incomplete ("TODO").
    """

    type: str = TypeEnum.taskItem.value
    attrs: NodeTaskItemAttrs = OPT
    content: list[BaseNode] = OPT

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return content_to_markdown(content=self.content, ignore_error=ignore_error)
