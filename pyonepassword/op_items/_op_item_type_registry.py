from json.decoder import JSONDecodeError
from typing import Any, Dict, Type, Union

from ..json import safe_unjson
from ..py_op_exceptions import OPInvalidItemException
from ._op_items_base import OPAbstractItem
from .item_validation_policy import OPItemValidationPolicy


class OPUnknownItemTypeException(Exception):
    def __init__(self, msg, item_dict=None):
        super().__init__(msg)
        self.item_dict = item_dict


class OPItemFactory:
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
    def _item_from_dict(cls, item_dict: Dict[str, Any], relaxed_validation: bool):
        if relaxed_validation:
            registry = cls._RELAXED_TYPE_REGISTRY
        else:
            registry = cls._TYPE_REGISTRY

        item_type = item_dict["category"]
        try:
            item_cls = registry[item_type]
        except KeyError as ke:
            raise OPUnknownItemTypeException(
                f"Unknown item type {item_type}", item_dict=item_dict) from ke

        obj = item_cls(item_dict)

        return obj

    @classmethod
    def op_item(cls, item_json_or_dict: Union[str, Dict], relaxed_validation=False):
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
        obj = cls._item_from_dict(item_dict, relaxed_validation)
        return obj

    @classmethod
    def item_class_relax_validation(cls, item_class: type):
        """
        Method to have the factory enable relaxed validation for 'item_class'

        Parameters
        ----------
        item_class : type
            Any OPAbstractItem class
        """
        cls._validate_item_class(item_class)
        OPItemValidationPolicy.set_relaxed_validation_for_class(item_class)

    @classmethod
    def item_class_strict_validation(cls, item_class: type):
        """
        Method to have the factory disable relaxed validation for 'item_class'

        Parameters
        ----------
        item_class : type
            any OPAbstractItem class
        """
        cls._validate_item_class(item_class)
        OPItemValidationPolicy.set_strict_validation_for_class(item_class)

    @classmethod
    def _validate_item_class(cls, item_class):
        # verify this is a registered item class
        try:
            item_class = cls._TYPE_REGISTRY[item_class.CATEGORY]
        except KeyError as ke:
            raise OPUnknownItemTypeException(
                f"Unknown item type {item_class.CATEGORY}") from ke
        except AttributeError:
            raise OPUnknownItemTypeException(
                f"Unknown item type: {item_class}")


def op_register_item_type(item_class):
    item_type = item_class.CATEGORY
    OPItemFactory.register_op_item_type(item_type, item_class)
    return item_class
