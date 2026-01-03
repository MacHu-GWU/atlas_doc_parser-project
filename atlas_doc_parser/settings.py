# -*- coding: utf-8 -*-

"""
Module-level settings for atlas_doc_parser.

These settings control the behavior of the library at runtime.
They can be modified at the module level to change default behavior.

Example::

    import atlas_doc_parser.settings as settings

    # Disable warnings for unimplemented types
    settings.WARN_UNIMPLEMENTED_TYPE = False

    # Now parse without warnings
    doc = NodeDoc.from_dict(data)
"""

# Whether to log warnings when encountering unimplemented node/mark types.
# When True (default), a warning will be logged to help users identify
# which types need to be implemented.
# When False, unimplemented types are silently skipped.
WARN_UNIMPLEMENTED_TYPE: bool = True
