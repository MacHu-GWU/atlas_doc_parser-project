# -*- coding: utf-8 -*-

import typing as T
import textwrap
import dataclasses

from func_args.api import REQ, OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseNode
from ..markdown_helpers import strip_double_empty_line, doc_content_to_markdown

if T.TYPE_CHECKING:  # pragma: no cover
    from .node_paragraph import NodeParagraph
    from .node_heading import NodeHeading
    from .node_bullet_list import NodeBulletList
    from .node_ordered_list import NodeOrderedList
    from .node_block_card import NodeBlockCard
    from .node_media_group import NodeMediaGroup
    from .node_media_single import NodeMediaSingle
    from .node_code_block import NodeCodeBlock
    from .node_task_list import NodeTaskList
    from .node_rule import NodeRule
    from .node_decision_list import NodeDecisionList
    from .node_extension import NodeExtension


@dataclasses.dataclass(frozen=True)
class NodePanelAttrs(Base):
    """
    Attributes for :class:`NodePanel`.

    :param panelType: Required. The visual style of the panel.
        One of: "info", "note", "tip", "warning", "error", "success", "custom".
    :param panelIcon: Optional. Custom icon for the panel (used with "custom" type).
    :param panelIconId: Optional. ID of the custom icon.
    :param panelIconText: Optional. Alt text for the panel icon.
    :param panelColor: Optional. Custom background color for the panel
        (used with "custom" type).
    :param localId: Optional. A unique identifier for the node.
    """

    panelType: T.Literal[
        "info",
        "note",
        "tip",
        "warning",
        "error",
        "success",
        "custom",
    ] = REQ
    panelIcon: str = OPT
    panelIconId: str = OPT
    panelIconText: str = OPT
    panelColor: str = OPT
    localId: str = OPT


@dataclasses.dataclass(frozen=True)
class NodePanel(BaseNode):
    """
    A container element for highlighting and visually distinguishing content.

    The panel node is a top-level block node that wraps content in a styled
    box to draw attention. Different panel types provide visual cues for
    different purposes:

    - **info**: General information (blue)
    - **note**: Additional notes (purple)
    - **tip**: Helpful tips (green)
    - **warning**: Caution notices (yellow)
    - **error**: Error messages (red)
    - **success**: Success messages (green)
    - **custom**: User-defined styling with custom icon and color

    Reference:
        https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/panel/
    """

    type: str = TypeEnum.panel.value
    attrs: NodePanelAttrs = REQ
    content: list[
        T.Union[
            "NodeParagraph",
            "NodeHeading",
            "NodeBulletList",
            "NodeOrderedList",
            "NodeBlockCard",
            "NodeMediaGroup",
            "NodeMediaSingle",
            "NodeCodeBlock",
            "NodeTaskList",
            "NodeRule",
            "NodeDecisionList",
            "NodeExtension",
        ]
    ] = REQ

    def to_markdown(
        self,
        ignore_error: bool = False,
    ) -> str:
        return (
            textwrap.indent(
                strip_double_empty_line(
                    "\n".join(
                        [
                            f"**{self.attrs.panelType.upper()}**",
                            "",
                            doc_content_to_markdown(
                                content=self.content,
                                ignore_error=ignore_error,
                            ),
                        ]
                    )
                ),
                prefix="> ",
                predicate=lambda line: True,
            )
            + "\n"
        )