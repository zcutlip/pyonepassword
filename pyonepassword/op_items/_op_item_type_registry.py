from json.decoder import JSONDecodeError
from typing import Any, Dict, Type, Union

from ..json import safe_unjson
from ..py_op_exceptions import OPInvalidItemException
from ._op_items_base import OPAbstractItem


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
    def _item_from_dict(cls, item_dict: Dict[str, Any]):
        item_type = item_dict["category"]
        try:
            item_cls = cls._TYPE_REGISTRY[item_type]
        except KeyError as ke:
            raise OPUnknownItemTypeException(
                f"Unknown item type {item_type}", item_dict=item_dict) from ke

        return item_cls(item_dict)

    @classmethod
    def op_item(cls, item_json_or_dict: Union[str, Dict]):
        try:
            item_dict = safe_unjson(item_json_or_dict)
        except JSONDecodeError as jdce:
            raise OPInvalidItemException(
                f"Failed to unserialize item JSON: {jdce}") from jdce
        obj = cls._item_from_dict(item_dict)
        return obj


def op_register_item_type(item_class):
    item_type = item_class.CATEGORY
    OPItemFactory.register_op_item_type(item_type, item_class)
    return item_class
