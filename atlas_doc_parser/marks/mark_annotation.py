# -*- coding: utf-8 -*-

import dataclasses

from func_args.api import OPT

from ..type_enum import TypeEnum
from ..mark_or_node import Base, BaseMark


class AnnotationType:
    """
    Valid values for the ``annotationType`` attribute.
    """

    inlineComment = "inlineComment"


@dataclasses.dataclass(frozen=True)
class MarkAnnotationAttrs(Base):
    """
    Attributes for :class:`MarkAnnotation`.

    :param id: Required. Unique identifier for the annotation.
    :param annotationType: Required. The type of annotation, currently only
        ``"inlineComment"`` is supported.
    """

    id: str = OPT
    annotationType: str = OPT


@dataclasses.dataclass(frozen=True)
class MarkAnnotation(BaseMark):
    """
    Marks text with an inline annotation (comment).

    The annotation mark is used to associate inline comments with specific
    text ranges in Confluence pages. When users highlight text and add a
    comment, the highlighted text is wrapped with this mark containing a
    unique ``id`` that links to the comment.
    """

    type: str = TypeEnum.annotation.value
    attrs: MarkAnnotationAttrs = OPT
