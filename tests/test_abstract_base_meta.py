"""
Tests for custom abstract base class support
"""
from typing import Dict, Union

import pytest

from pyonepassword.op_items.item_types._item_base import OPAbstractItem
from pyonepassword.op_items.item_types._item_descriptor_base import (
    OPAbstractItemDescriptor
)

from .fixtures.valid_data import ValidData

VALID_INPUT_ITEM = "example-login-with-fields"


def test_abc_meta_01(valid_data: ValidData):
    """
    Test:
      - instantiating an Abstract Base Class with a method requiring implementation

    Verify:
        - TypeError is raised
    """
    item_dict = valid_data.data_for_name(VALID_INPUT_ITEM)

    with pytest.raises(TypeError):
        OPAbstractItemDescriptor(item_dict)


def test_abc_meta_02(valid_data: ValidData):
    """
    Test:
      - instantiating a class extending an ABC with that does not implement all enforced methods

    Verify:
        - Subclass is still abstract and TypeError is raised
    """
    item_dict = valid_data.data_for_name(VALID_INPUT_ITEM)

    with pytest.raises(TypeError):
        OPAbstractItem(item_dict)


def test_abc_meta_03(valid_data: ValidData):
    """
    Test:
      - instantiating a class extending an ABC with that does not implement all enforced methods

    Verify:
        - Subclass is still abstract and TypeError is raised
    """
    class OPConcreteItem(OPAbstractItem):
        """
        A subclass of an ABC that properly implements the enforced __init__() method
        """

        def __init__(self, item_dict_or_json: Union[Dict, str]):
            super().__init__(item_dict_or_json)

    item_dict = valid_data.data_for_name(VALID_INPUT_ITEM)

    # No error/exception should be raised, since enforced methods have been implemented
    OPConcreteItem(item_dict)
