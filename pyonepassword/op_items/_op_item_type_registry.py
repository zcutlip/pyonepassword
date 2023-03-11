from json.decoder import JSONDecodeError
from typing import Any, Dict, Type, Union

from ..json import safe_unjson
from ..py_op_exceptions import OPInvalidItemException
from .item_types._item_base import OPAbstractItem
from .item_types._item_descriptor_base import OPAbstractItemDescriptor
from .item_types.generic_item import (
    _OPGenericItem,
    _OPGenericItemDescriptor,
    _OPGenericItemRelaxedValidation
)


class OPUnknownItemTypeException(Exception):
    def __init__(self, msg, item_dict=None):
        super().__init__(msg)
        self.item_dict = item_dict


GenericType = Union[Type[_OPGenericItemDescriptor],
                    Type[_OPGenericItem]]


class OPItemFactory:
    # Fallback class for when item is an unknown types and caller
    # has enabled generic items
    _GENERIC_ITEM_CLASS: GenericType = _OPGenericItem

    # Fallback class when caller has enabled generic items as well as
    # relaxed item validation
    _GENERIC_ITEM_CLASS_RELAXED_VALIDATION = _OPGenericItemRelaxedValidation
    # registry of item classes with strict validation
    _TYPE_REGISTRY: Dict[str, Type[OPAbstractItem]] = {}
    # registry of item classes with relaxed validation
    _RELAXED_TYPE_REGISTRY: Dict[str, Type[OPAbstractItem]] = {}

    @classmethod
    def register_op_item_type(cls, item_type: str, item_class: Type[OPAbstractItem]):
        """
        Register an OP item type class

        If the class has the _relaxed_validation attribute set to True, it will be added
        to the registry of relaxed validation classes, otherwise it is added to the
        normal registry

        Parameters
        ----------
        item_type : str
            The CATEGORY attribute of the class representing the item type, such as "LOGIN"
        item_class : Type[OPAbstractItem]
            The item type class to register

        Raises
        ------
        Exception
            If two item type classes with the same CATEGORY are registered
        """
        if getattr(item_class, "_relaxed_validation", False):
            registry = cls._RELAXED_TYPE_REGISTRY
        else:
            registry = cls._TYPE_REGISTRY

        if item_type in registry:
            raise Exception(  # pragma: no coverage
                f"duplicate for item type {item_type}: {item_class}")
        registry[item_type] = item_class

    @classmethod
    def _item_from_dict(cls, item_dict: Dict[str, Any], generic_okay: bool = False, relaxed_validation: bool = False):
        generic_item_class: GenericType
        if relaxed_validation:
            registry = cls._RELAXED_TYPE_REGISTRY
            generic_item_class = cls._GENERIC_ITEM_CLASS_RELAXED_VALIDATION
        else:
            registry = cls._TYPE_REGISTRY
            generic_item_class = cls._GENERIC_ITEM_CLASS

        item_type = item_dict["category"]
        item_cls: Type[OPAbstractItemDescriptor]
        try:
            item_cls = registry[item_type]
        except KeyError as ke:
            if generic_okay:
                item_cls = generic_item_class
            else:
                raise OPUnknownItemTypeException(
                    f"Unknown item type {item_type}", item_dict=item_dict) from ke

        obj = item_cls(item_dict)

        return obj

    @classmethod
    def op_item(cls, item_json_or_dict: Union[str, Dict], generic_okay: bool = False, relaxed_validation: bool = False):
        """
        Factory methiod to instantiate an op item from JSON or a dictionary

        Parameters
        ----------
        item_json_or_dict : Union[str, Dict]
            JSON or dictionary representing an op item object
        relaxed_validation : bool, optional
            Whether relaxed validation should be enabled for this instance, by default False
            If true, the item class will be looked up from the relaxed validation registry

        Returns
        -------
        OPAbstractItem
            An instance of OPAbstractItem representing the 1Password item object

        Raises
        ------
        OPInvalidItemException
            If unserializing JSON fails, or the dictionary is otherwise invalid for an item object
        """
        try:
            item_dict = safe_unjson(item_json_or_dict)
        except JSONDecodeError as jdce:
            raise OPInvalidItemException(
                f"Failed to unserialize item JSON: {jdce}") from jdce
        obj = cls._item_from_dict(
            item_dict, generic_okay=generic_okay, relaxed_validation=relaxed_validation)
        return obj


def op_register_item_type(item_class):
    item_type = item_class.CATEGORY
    OPItemFactory.register_op_item_type(item_type, item_class)
    return item_class
