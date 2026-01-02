@ -1,250 +0,0 @@
# -*- coding: utf-8 -*-

"""
Base classes for ADF data model.

This module provides the foundational classes for deserializing Atlassian Document
Format (ADF) JSON into Python objects:

- ``Base``: Base class for all dataclasses
- ``BaseMark``: Base class for text marks (formatting)
- ``BaseNode``: Base class for document nodes
"""

import typing as T
import copy
import dataclasses

from func_args.api import BaseFrozenModel, REQ, OPT, remove_optional

from .type_hint import T_DATA

T_FIELDS = dict[str, dataclasses.Field]
_CLASS_FIELD: dict[T.Any, T_FIELDS] = {}  # class fields cache


@dataclasses.dataclass(frozen=True)
class Base(BaseFrozenModel):
    """
    Base class for all ADF dataclasses.

    Provides common functionality:
    - ``from_dict()``: Deserialize from dictionary
    - ``to_dict()``: Serialize to dictionary
    """

    @classmethod
    def get_fields(cls) -> T_FIELDS:
        """
        Get the dict view of the ``dataclasses.Field`` in this class.
        It leverages the cache to avoid the overhead of ``dataclasses.fields``
        function call.
        """
        try:
            return _CLASS_FIELD[cls]
        except KeyError:
            _CLASS_FIELD[cls] = {field.name: field for field in dataclasses.fields(cls)}
            return _CLASS_FIELD[cls]

    def to_dict(self) -> T_DATA:
        """
        Convert the dataclass to a complete dictionary with all fields.
        """
        return remove_optional(**dataclasses.asdict(self))

    def to_kwargs(self) -> T_DATA:
        """
        Convert the dataclass to a dictionary suitable for function calls.
        """
        return self.to_dict()

    @classmethod
    def from_dict(cls, dct: T_DATA) -> "Base":
        """
        Construct an instance from a dictionary.

        Only fields defined in the dataclass will be used.

        This is a defensive programming practice: it ensures that only fields defined
        in the dataclass are used when constructing an instance from a dictionary.
        This is important because the Atlassian Document Format may introduce
        new fields over time, and if the library is outdated, unexpected fields
        could be present in the input data. By ignoring unknown fields, the code
        remains robust and avoids errors due to schema changes.
        """
        _fields = cls.get_fields()
        kwargs = {}
        for field_name, field in _fields.items():
            try:
                kwargs[field_name] = dct[field_name]
            except KeyError:
                pass
        return cls(**kwargs)

    def is_opt(self, value: T.Any) -> bool:
        return value is OPT

T_BASE = T.TypeVar("T_BASE", bound=Base)


# =============================================================================
# BaseMark Class
# =============================================================================
@dataclasses.dataclass(frozen=True)
class BaseMark(Base):
    """
    Base class for ADF marks (text formatting).

    Marks represent formatting applied to text nodes, such as:
    - ``strong`` (bold)
    - ``em`` (italic)
    - ``link`` (hyperlink)
    - ``code`` (inline code)

    Subclasses should override ``to_markdown()`` to provide format conversion.
    """

    type: str = dataclasses.field(default_factory=REQ)

    @classmethod
    def from_dict(cls: T.Type["T_MARK"], dct: T_DATA) -> "T_MARK":
        """
        Deserialize from dictionary.

        Handles nested ``attrs`` deserialization if the subclass defines an
        ``attrs`` field with a type that has ``from_dict()``.
        """
        dct = copy.deepcopy(dct)
        if "attrs" in dct:
            fields = cls.get_fields()
            if "attrs" in fields:
                attrs_field = fields["attrs"]
                # Check if attrs field type has from_dict method
                if hasattr(attrs_field.type, "from_dict"):
                    dct["attrs"] = attrs_field.type.from_dict(dct["attrs"])
        return super().from_dict(dct)

    def to_dict(self) -> T_DATA:
        """Serialize to dictionary, handling nested attrs."""
        data = super().to_dict()
        if "attrs" in data and hasattr(data["attrs"], "to_dict"):
            data["attrs"] = remove_optional(**data["attrs"])
        return data

    def to_markdown(self, text: str) -> str:
        """
        Apply this mark's formatting to text.

        Subclasses should override this method.
        Default implementation returns text unchanged.
        """
        return text


T_MARK = T.TypeVar("T_MARK", bound=BaseMark)


# =============================================================================
# BaseNode Class
# =============================================================================
@dataclasses.dataclass(frozen=True)
class BaseNode(Base):
    """
    Base class for ADF nodes (document structure elements).

    Nodes represent structural elements of the document, such as:
    - Block nodes: ``paragraph``, ``heading``, ``codeBlock``, ``table``
    - Inline nodes: ``text``, ``mention``, ``emoji``

    Nodes can contain:
    - ``attrs``: Node-specific attributes
    - ``content``: Child nodes (for container nodes)
    - ``marks``: Text formatting (for inline nodes)

    Subclasses should override ``to_markdown()`` to provide format conversion.
    """

    type: str = dataclasses.field(default_factory=REQ)

    @classmethod
    def from_dict(
        cls: T.Type["T_NODE"],
        dct: T_DATA,
        ignore_error: bool = False,
    ) -> "T_NODE":
        """
        Deserialize from dictionary.

        Handles nested deserialization of:
        - ``attrs``: Using the field type's ``from_dict()``
        - ``content``: Using ``parse_node()`` for each child
        - ``marks``: Using ``parse_mark()`` for each mark
        """
        from .parse import parse_mark, parse_node

        dct = copy.deepcopy(dct)

        # Deserialize attrs
        if "attrs" in dct:
            fields = cls.get_fields()
            if "attrs" in fields:
                attrs_field = fields["attrs"]
                if hasattr(attrs_field.type, "from_dict"):
                    dct["attrs"] = attrs_field.type.from_dict(dct["attrs"])

        # Deserialize content (child nodes)
        if "content" in dct:
            if isinstance(dct["content"], list) and parse_node is not None:
                new_content = []
                for d in dct["content"]:
                    try:
                        content = parse_node(d)
                        new_content.append(content)
                    except Exception as e:
                        if ignore_error:
                            pass
                        else:
                            raise e
                dct["content"] = new_content

        # Deserialize marks
        if "marks" in dct:
            if isinstance(dct["marks"], list) and parse_mark is not None:
                new_marks = []
                for d in dct["marks"]:
                    mark = parse_mark(d)
                    new_marks.append(mark)
                dct["marks"] = new_marks

        return super().from_dict(dct)

    def to_dict(self) -> T_DATA:
        """Serialize to dictionary, handling nested attrs, content, and marks."""
        # Build dict directly without modifying the frozen instance
        data = dataclasses.asdict(self)

        # Serialize attrs
        if "attrs" in data and data["attrs"] is not OPT:
            if hasattr(self.attrs, "to_dict"):
                data["attrs"] = self.attrs.to_dict()

        # Serialize content
        if "content" in data and data["content"] is not OPT:
            data["content"] = [c.to_dict() for c in self.content]

        # Serialize marks
        if "marks" in data and data["marks"] is not OPT:
            data["marks"] = [m.to_dict() for m in self.marks]

        return remove_optional(**data)

    def to_markdown(self, ignore_error: bool = False) -> str:
        """
        Convert this node to Markdown format.

        Subclasses should override this method.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} has not implemented ``to_markdown()``"
        )


T_NODE = T.TypeVar("T_NODE", bound=BaseNode)