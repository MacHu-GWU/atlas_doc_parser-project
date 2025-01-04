# -*- coding: utf-8 -*-

import typing as T
import enum
import copy
import textwrap
import dataclasses
from datetime import datetime

from .constants import TAB
from .arg import REQ, NA, rm_na
from .type_enum import TypeEnum
from .base import Base, T_DATA, T_DATA_LIKE


@dataclasses.dataclass
class BaseMark(Base):
    type: str = dataclasses.field(default_factory=REQ)

    @classmethod
    def from_dict(
        cls: T.Type["T_MARK"],
        dct: T_DATA,
    ) -> "T_MARK":
        # print(f"{dct = }")  # for debug only
        dct = copy.deepcopy(dct)
        if "attrs" in dct:
            fields = cls.get_fields()
            attrs_field = fields["attrs"]
            dct["attrs"] = attrs_field.type.from_dict(dct["attrs"])
        return super().from_dict(dct)

    def to_dict(self) -> T_DATA:
        data = super().to_dict()
        if "attrs" in data:
            data["attrs"] = rm_na(**data["attrs"])
        return data

    def to_markdown(self, text: str) -> str:
        return text


T_MARK = T.TypeVar("T_MARK", bound=BaseMark)


@dataclasses.dataclass
class MarkBackGroundColorAttrs(Base):
    color: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class MarkBackGroundColor(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.backgroundColor.value)
    attrs: MarkBackGroundColorAttrs = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class MarkCode(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.code.value)

    def to_markdown(self, text: str) -> str:
        return f"`{text}`"


@dataclasses.dataclass
class MarkEm(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.em.value)

    def to_markdown(self, text: str) -> str:
        return f"*{text}*"


@dataclasses.dataclass
class MarkLinkAttrs(Base):
    href: str = dataclasses.field(default_factory=REQ)
    title: str = dataclasses.field(default_factory=NA)
    id: str = dataclasses.field(default_factory=NA)
    collection: str = dataclasses.field(default_factory=NA)
    occurrenceKey: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class MarkLink(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.link.value)
    attrs: MarkLinkAttrs = dataclasses.field(default_factory=REQ)

    def to_markdown(self, text: str) -> str:
        if isinstance(self.attrs.title, str):
            title = self.attrs.title
        else:
            title = text
        return f"[{title}]({self.attrs.href})"


@dataclasses.dataclass
class MarkStrike(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.strike.value)

    def to_markdown(self, text: str) -> str:
        return f"~~{text}~~"


@dataclasses.dataclass
class MarkStrong(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.strong.value)

    def to_markdown(self, text: str) -> str:
        return f"**{text}**"


@dataclasses.dataclass
class MarkSubSupAttrs(Base):
    type: str = dataclasses.field(default=TypeEnum.sub.value)


@dataclasses.dataclass
class MarkSubSup(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.subsup.value)
    attrs: MarkSubSupAttrs = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class MarkTextColorAttrs(Base):
    color: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class MarkTextColor(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.textColor.value)
    attrs: MarkTextColorAttrs = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class MarkUnderLine(BaseMark):
    type: str = dataclasses.field(default=TypeEnum.underline.value)


_mark_type_to_class_mapping = {
    TypeEnum.backgroundColor.value: MarkBackGroundColor,
    TypeEnum.code.value: MarkCode,
    TypeEnum.em.value: MarkEm,
    TypeEnum.link.value: MarkLink,
    TypeEnum.strike.value: MarkStrike,
    TypeEnum.strong.value: MarkStrong,
    TypeEnum.subsup.value: MarkSubSup,
    TypeEnum.textColor.value: MarkTextColor,
    TypeEnum.underline.value: MarkUnderLine,
}


def parse_mark(dct: T_DATA) -> "T_MARK":
    # print(f"{dct = }")  # for debug only
    type_ = dct["type"]
    klass = _mark_type_to_class_mapping[type_]
    # print(f"{klass = }")  # for debug only
    return klass.from_dict(dct)


@dataclasses.dataclass
class BaseNode(Base):
    type: str = dataclasses.field(default_factory=REQ)

    @classmethod
    def from_dict(
        cls: T.Type["T_NODE"],
        dct: T_DATA,
        ignore_error: bool = False,
    ) -> "T_NODE":
        # print(f"{dct = }")  # for debug only
        dct = copy.deepcopy(dct)

        if "attrs" in dct:
            fields = cls.get_fields()
            attrs_field = fields["attrs"]
            dct["attrs"] = attrs_field.type.from_dict(dct["attrs"])

        if "content" in dct:
            if isinstance(dct["content"], list):
                new_content = list()
                for d in dct["content"]:
                    # print(f"{d = }")  # for debug only
                    # impl 1. use try except
                    # try:
                    #     content = parse_node(d)
                    #     new_content.append(content)
                    # except Exception as e:
                    #     if ignore_error:
                    #         pass
                    #     else:
                    #         raise e
                    # impl 2. no try except, for debug only
                    content = parse_node(d)
                    new_content.append(content)

                dct["content"] = new_content

        if "marks" in dct:
            if isinstance(dct["marks"], list):
                new_marks = list()
                for d in dct["marks"]:
                    # print(f"{d = }")  # for debug only
                    mark = parse_mark(d)
                    new_marks.append(mark)
                dct["marks"] = new_marks

        # print(f"{dct = }")  # for debug only
        return super().from_dict(dct)

    def to_dict(self) -> T_DATA:
        inst = copy.copy(self)
        if hasattr(inst, "attrs"):
            if isinstance(inst.attrs, NA) is False:
                inst.attrs = inst.attrs.to_dict()
        if hasattr(inst, "content"):
            if isinstance(inst.content, NA) is False:
                inst.content = [c.to_dict() for c in inst.content]
        if hasattr(inst, "marks"):
            if isinstance(inst.marks, NA) is False:
                inst.marks = [m.to_dict() for m in inst.marks]
        data = dataclasses.asdict(inst)
        return rm_na(**data)

    def to_markdown(self) -> str:
        raise NotImplementedError(
            f"{self.__class__.__name__} has not implemented the ``def to_markdown(self):`` method"
        )


T_NODE = T.TypeVar("T_NODE", bound=BaseNode)


def _strip_double_empty_line(text: str, n: int = 3) -> str:
    for _ in range(n):
        text = text.replace("\n\n\n", "\n\n")
    return text


def _content_to_markdown(
    content: T.Union[T.List["T_NODE"], NA],
    concat: str = "",
) -> str:
    """
    Concatenate the markdown of the content.
    """
    if isinstance(content, NA):
        return ""
    else:
        lst = list()
        for node in content:
            # print("----- Work on a new node -----")
            md = node.to_markdown()
            # print(f"{node = }")
            # print(f"{md = }")
            lst.append(md)
        return concat.join(lst)


def _doc_content_to_markdown(
    content: T.Union[T.List["T_NODE"], NA],
    concat: str = "\n",
) -> str:
    if isinstance(content, NA):
        return ""
    else:
        lst = list()
        for node in content:
            # print("----- Work on a new node -----")
            if isinstance(node, (NodeBulletList, NodeOrderedList, NodeCodeBlock)):
                md = "\n" + node.to_markdown() + "\n"
            else:
                md = node.to_markdown()
            # print(f"{node = }")
            # print(f"{md = }")
            lst.append(md)

    md = _strip_double_empty_line(concat.join(lst))
    return md


@dataclasses.dataclass
class NodeBlockQuote(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.blockquote.value)
    content: T.List["T_NODE"] = dataclasses.field(default_factory=NA)

    def to_markdown(self) -> str:
        return (
            textwrap.indent(
                _doc_content_to_markdown(self.content),
                prefix="> ",
                predicate=lambda line: True,
            )
            + "\n"
        )


@dataclasses.dataclass
class NodeBulletList(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.bulletList.value)
    content: T.List["T_NODE"] = dataclasses.field(default_factory=REQ)

    def to_markdown(
        self,
        level: int = 0,
    ) -> str:
        lines = []
        indent = "    " * level  # 4 spaces per level

        for item in self.content:
            if isinstance(item, NodeListItem):
                # Process the list item content
                content_lines = []
                for node in item.content:
                    if isinstance(node, NodeBulletList):
                        # Nested list - increase level
                        content_lines.append(node.to_markdown(level=level + 1))
                    else:
                        # Regular content (like paragraph)
                        content_lines.append(node.to_markdown().rstrip())

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


@dataclasses.dataclass
class NodeCodeBlockAttrs(Base):
    language: str = dataclasses.field(default_factory=NA)


_atlassian_lang_to_markdown_lang_mapping = {}


@dataclasses.dataclass
class NodeCodeBlock(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.codeBlock.value)
    attrs: NodeCodeBlockAttrs = dataclasses.field(default_factory=NA)
    content: T.List["T_NODE"] = dataclasses.field(default_factory=NA)

    def to_markdown(self) -> str:
        code = _content_to_markdown(self.content)
        lang = ""
        if isinstance(self.attrs, NodeCodeBlockAttrs):
            if isinstance(self.attrs.language, str):
                lang = _atlassian_lang_to_markdown_lang_mapping.get(
                    self.attrs.language,
                    self.attrs.language,
                )
        return f"```{lang}\n{code}\n```"


@dataclasses.dataclass
class NodeDateAttrs(Base):
    timestamp: str = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class NodeDate(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.date.value)
    attrs: NodeDateAttrs = dataclasses.field(default_factory=REQ)

    def to_markdown(self) -> str:
        return str(datetime.utcfromtimestamp(int(self.attrs.timestamp) / 1000).date())


@dataclasses.dataclass
class NodeDoc(BaseNode):
    version: int = dataclasses.field(default=1)
    type: str = dataclasses.field(default=TypeEnum.doc.value)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        md = _doc_content_to_markdown(self.content)
        return md


@dataclasses.dataclass
class NodeEmojiAttrs(Base):
    shortName: str = dataclasses.field(default_factory=REQ)
    id: str = dataclasses.field(default_factory=NA)
    text: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeEmoji(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.emoji.value)
    attrs: NodeEmojiAttrs = dataclasses.field(default_factory=REQ)

    def to_markdown(self) -> str:
        if isinstance(self.attrs.text, str):
            return self.attrs.text
        else:
            raise NotImplementedError


@dataclasses.dataclass
class NodeExpandAttrs(Base):
    title: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeExpand(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.expand.value)
    attrs: NodeExpandAttrs = dataclasses.field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)
    marks: T.List["T_MARK"] = dataclasses.field(default=NA)

    def to_markdown(self) -> str:
        return _doc_content_to_markdown(self.content)


@dataclasses.dataclass
class NodeHardBreak(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.hardBreak.value)


@dataclasses.dataclass
class NodeHeadingAttrs(Base):
    level: int = dataclasses.field(default_factory=REQ)
    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeHeading(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.heading.value)
    attrs: NodeHeadingAttrs = dataclasses.field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        """
        For heading, we would like to have an empty line before and after the heading.
        """
        md = (
            "\n\n"
            + "{} {}".format(
                "#" * self.attrs.level,
                _content_to_markdown(self.content),
            )
            + "\n\n"
        )
        return md


@dataclasses.dataclass
class NodeInlineCardAttrs(Base):
    url: str = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class NodeInlineCard(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.inlineCard.value)
    attrs: NodeInlineCardAttrs = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class NodeListItem(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.listItem.value)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return _content_to_markdown(self.content)


@dataclasses.dataclass
class NodeMediaAttrs(Base):
    id: str = dataclasses.field(default_factory=NA)
    type: str = dataclasses.field(default_factory=REQ)
    collection: str = dataclasses.field(default_factory=NA)
    width: int = dataclasses.field(default_factory=NA)
    height: int = dataclasses.field(default_factory=NA)
    occurrenceKey: int = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeMedia(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.media.value)
    attrs: NodeMediaAttrs = dataclasses.field(default_factory=REQ)
    marks: T.List["T_MARK"] = dataclasses.field(default=NA)

    def to_markdown(self) -> str:
        return ""


@dataclasses.dataclass
class NodeMediaGroup(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.mediaGroup.value)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return ""


@dataclasses.dataclass
class NodeMediaSingleAttrs(Base):
    layout: str = dataclasses.field(default_factory=REQ)
    width: float = dataclasses.field(default_factory=NA)
    widthType: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeMediaSingle(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.mediaSingle.value)
    attrs: NodeMediaSingleAttrs = dataclasses.field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return _content_to_markdown(self.content)


@dataclasses.dataclass
class NodeMentionAttrs(Base):
    id: str = dataclasses.field(default_factory=REQ)
    text: str = dataclasses.field(default_factory=NA)
    userType: str = dataclasses.field(default_factory=NA)
    accessLevel: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeMention(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.mention.value)
    attrs: NodeMentionAttrs = dataclasses.field(default_factory=REQ)

    def to_markdown(self) -> str:
        if isinstance(self.attrs.text, NA):
            return "@Unknown"
        else:
            return self.attrs.text


@dataclasses.dataclass
class NodeNestedExpandAttrs(Base):
    title: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeNestedExpand(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.nestedExpand.value)
    attrs: NodeNestedExpandAttrs = dataclasses.field(default_factory=NA)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)


@dataclasses.dataclass
class NodeOrderedListAttrs(Base):
    order: int = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeOrderedList(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.orderedList.value)
    attrs: NodeOrderedListAttrs = dataclasses.field(default_factory=NA)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(
        self,
        level: int = 0,
    ) -> str:
        lines = []
        indent = "    " * level  # 4 spaces per level

        # Start numbering from attrs.order (or 1 for inner levels)
        if level == 0 and isinstance(self.attrs.order, int):
            current_num = self.attrs.order
        else:
            current_num = 1

        for item in self.content:
            if isinstance(item, NodeListItem):
                # Process the list item content
                content_lines = []
                for node in item.content:
                    if isinstance(node, NodeOrderedList):
                        # Nested list - increase level
                        content_lines.append(node.to_markdown(level=level + 1))
                    else:
                        # Regular content (like paragraph)
                        content_lines.append(node.to_markdown().rstrip())

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


@dataclasses.dataclass
class NodePanelAttrs(Base):
    panelType: str = dataclasses.field(default_factory=REQ)


@dataclasses.dataclass
class NodePanel(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.panel.value)
    attrs: NodePanelAttrs = dataclasses.field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default=REQ)

    def to_markdown(self) -> str:
        return (
            textwrap.indent(
                _strip_double_empty_line(
                    "\n".join(
                        [
                            f"**{self.attrs.panelType.upper()}**",
                            "",
                            _doc_content_to_markdown(self.content),
                        ]
                    )
                ),
                prefix="> ",
                predicate=lambda line: True,
            )
            + "\n"
        )


@dataclasses.dataclass
class NodeParagraphAttrs(Base):
    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeParagraph(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.paragraph.value)
    attrs: NodeParagraphAttrs = dataclasses.field(default_factory=NA)
    content: T.List["T_NODE"] = dataclasses.field(default_factory=NA)

    def to_markdown(self) -> str:
        return _content_to_markdown(self.content) + "\n"


@dataclasses.dataclass
class NodeRule(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.rule.value)

    def to_markdown(self) -> str:
        return "---"


@dataclasses.dataclass
class NodeStatusAttrs(Base):
    text: str = dataclasses.field(default_factory=REQ)
    color: str = dataclasses.field(default="neutral")
    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeStatus(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.status.value)
    attrs: NodeStatusAttrs = dataclasses.field(default_factory=REQ)

    def to_markdown(self) -> str:
        return f"`{self.attrs.text}`"


@dataclasses.dataclass
class NodeTable(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.table.value)


@dataclasses.dataclass
class NodeTableCell(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.tableCell.value)


@dataclasses.dataclass
class NodeTableHeader(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.tableHeader.value)


@dataclasses.dataclass
class NodeTableRow(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.tableRow.value)


@dataclasses.dataclass
class NodeHeadingAttrs(Base):
    level: int = dataclasses.field(default_factory=REQ)
    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeTaskItemAttrs(Base):
    """Attributes for task item node."""

    state: str = dataclasses.field(default_factory=REQ)
    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeTaskItem(BaseNode):
    """Task item node representing a single task."""

    type: str = dataclasses.field(default=TypeEnum.taskItem.value)
    attrs: NodeTaskItemAttrs = dataclasses.field(default_factory=REQ)
    content: T.List["T_NODE"] = dataclasses.field(default_factory=REQ)

    def to_markdown(self) -> str:
        # Convert state to checkbox representation
        checkbox = "[x]" if self.attrs.state == "DONE" else "[ ]"
        return f"{checkbox} {_content_to_markdown(self.content)}"


@dataclasses.dataclass
class NodeTaskListAttrs(Base):
    """Attributes for task list node."""

    localId: str = dataclasses.field(default_factory=NA)


@dataclasses.dataclass
class NodeTaskList(BaseNode):
    """Container for task items."""

    type: str = dataclasses.field(default=TypeEnum.taskList.value)
    attrs: NodeTaskListAttrs = dataclasses.field(default_factory=NA)
    content: list[T.Union[NodeTaskItem, "NodeTaskList"]] = dataclasses.field(
        default_factory=REQ
    )

    def _to_markdown(
        self,
        level: int = 0,
        lines: T.Optional[T.List[str]] = None,
    ) -> list[str]:
        indent = TAB * level
        if lines is None:
            lines = []
        for task_item_or_task_list in self.content:
            if isinstance(task_item_or_task_list, NodeTaskItem):
                task_item = task_item_or_task_list
                lines.append(f"{indent}- {task_item.to_markdown()}")
            elif isinstance(task_item_or_task_list, NodeTaskList):
                task_list = task_item_or_task_list
                task_list._to_markdown(level=level + 1, lines=lines)
            else:
                raise TypeError(f"Unexpected type: {type(task_item_or_task_list)}")
        return lines

    def to_markdown(self) -> str:
        lines = self._to_markdown()
        return "\n".join(lines)


@dataclasses.dataclass
class NodeText(BaseNode):
    type: str = dataclasses.field(default=TypeEnum.text.value)
    text: str = dataclasses.field(default_factory=REQ)
    marks: T.List["T_MARK"] = dataclasses.field(default_factory=NA)

    def to_markdown(self):
        md = self.text
        if isinstance(self.marks, list):
            for mark in self.marks:
                md = mark.to_markdown(md)
        return md


_node_type_to_class_mapping = {
    TypeEnum.blockquote.value: NodeBlockQuote,
    TypeEnum.bulletList.value: NodeBulletList,
    TypeEnum.codeBlock.value: NodeCodeBlock,
    TypeEnum.date.value: NodeDate,
    TypeEnum.doc.value: NodeDoc,
    TypeEnum.emoji.value: NodeEmoji,
    TypeEnum.expand.value: NodeExpand,
    TypeEnum.hardBreak.value: NodeHardBreak,
    TypeEnum.heading.value: NodeHeading,
    TypeEnum.inlineCard.value: NodeInlineCard,
    TypeEnum.listItem.value: NodeListItem,
    TypeEnum.media.value: NodeMedia,
    TypeEnum.mediaGroup.value: NodeMediaGroup,
    TypeEnum.mediaSingle.value: NodeMediaSingle,
    TypeEnum.mention.value: NodeMention,
    TypeEnum.nestedExpand.value: NodeNestedExpand,
    TypeEnum.orderedList.value: NodeOrderedList,
    TypeEnum.panel.value: NodePanel,
    TypeEnum.paragraph.value: NodeParagraph,
    TypeEnum.rule.value: NodeRule,
    TypeEnum.status.value: NodeStatus,
    TypeEnum.table.value: NodeTable,
    TypeEnum.tableCell.value: NodeTableCell,
    TypeEnum.tableHeader.value: NodeTableHeader,
    TypeEnum.tableRow.value: NodeTableRow,
    TypeEnum.taskList.value: NodeTaskList,
    TypeEnum.taskItem.value: NodeTaskItem,
    TypeEnum.text.value: NodeText,
}


def parse_node(dct: T_DATA) -> "T_NODE":
    # print(f"{dct = }")  # for debug only
    type_ = dct["type"]
    klass = _node_type_to_class_mapping[type_]
    # print(f"{klass = }")  # for debug only
    return klass.from_dict(dct)
