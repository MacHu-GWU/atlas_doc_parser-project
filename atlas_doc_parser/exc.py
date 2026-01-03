# -*- coding: utf-8 -*-

"""
Exceptions for atlas_doc_parser.
"""


class ParamError(Exception):
    """Raised when a parameter validation fails."""

    pass


class UnimplementedTypeError(Exception):
    """
    Raised when an ADF node or mark type is not yet implemented.

    This exception is used to gracefully handle unimplemented types during parsing.
    When a type is not registered in the type-to-class mapping, this exception
    is raised and can be caught to skip the unimplemented element.

    Attributes:
        type_value: The unimplemented type string (e.g., "bodiedExtension").
        category: Either "node" or "mark" indicating which type is missing.

    Example:
        >>> raise UnimplementedTypeError("bodiedExtension", "node")
        UnimplementedTypeError: Node type 'bodiedExtension' is not yet implemented.
        Please submit an issue at https://github.com/MacHu-GWU/atlas_doc_parser-project/issues
        with this type name so it can be added in a future release.
    """

    def __init__(self, type_value: str, category: str):
        self.type_value = type_value
        self.category = category
        super().__init__(
            f"{category.capitalize()} type '{type_value}' is not yet implemented. "
            f"Please submit an issue at https://github.com/MacHu-GWU/atlas_doc_parser-project/issues "
            f"with this type name so it can be added in a future release."
        )
