from ._item_base import OPAbstractItem
from ._item_descriptor_base import OPAbstractItemDescriptor

"""
This module contains classes that may optionally be used as stand-ins for unknown
item and item descriptor types

These classes are not exposed as API as they are not intended to be used directly

Rather, the caller should pass the appropriate flags to API methods to enable their use
"""


class _OPGenericItemDescriptor(OPAbstractItemDescriptor):
    """
    A generic item descriptor class that can optionally be used as a fallback
    when an item descriptor list contains an unknown item type
    """

    def __init__(self, item_dict_or_json):
        super().__init__(item_dict_or_json)


class _OPGenericItem(OPAbstractItem):  # pragma: no coverage
    """
    A generic item class that can optionally be used as a fallback when
    retrieving an item of unknown type
    """

    def __init__(self, item_dict_or_json):
        super().__init__(item_dict_or_json)


class _OPGenericItemRelaxedValidation(_OPGenericItem):
    """
    A relaxed validation of _OPGenericItem that will allow creation of item objects
    from non-conformant item dictionaries

    This class is not intended to be used directly (publically or internally). It
    is registered with
    """
    _relaxed_validation = True
