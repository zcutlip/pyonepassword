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
    _TYPE_REGISTRY: Dict[str, Type[OPAbstractItem]] = {}

    @classmethod
    def register_op_item_type(cls, item_type, item_class):
        if item_type in cls._TYPE_REGISTRY:
            raise Exception(  # pragma: no coverage
                f"duplicate for item type {item_type}: {item_class}")
        cls._TYPE_REGISTRY[item_type] = item_class

    @classmethod
    def _item_from_dict(cls, item_dict: Dict[str, Any], relaxed_validation: bool):
        item_type = item_dict["category"]
        try:
            item_cls = cls._TYPE_REGISTRY[item_type]
        except KeyError as ke:
            raise OPUnknownItemTypeException(
                f"Unknown item type {item_type}", item_dict=item_dict) from ke

        # get the existing validation policy for item_cls so we can restore it later
        saved_validation_policy = OPItemValidationPolicy.get_relaxed_validation_for_class(
            item_cls)

        if relaxed_validation:
            # enable relaxed validation for this class if we were asked to
            cls.item_class_relax_validation(item_cls)

        obj = item_cls(item_dict)
        if relaxed_validation and not saved_validation_policy:
            # if we were asked to relax validation, and it wasn't relaxed when we started
            # set it back to stric
            cls.item_class_strict_validation(item_cls)

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
