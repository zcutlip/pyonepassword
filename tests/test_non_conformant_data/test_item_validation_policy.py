from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.non_comformant_data import NonConformantData

from pyonepassword.api.exceptions import (
    OPInvalidItemException,
    OPSectionCollisionException
)
from pyonepassword.api.object_types import OPLoginItem
from pyonepassword.api.validation import (
    disable_relaxed_validation,
    enable_relaxed_validation,
    get_relaxed_validation,
    get_relaxed_validation_for_class,
    set_relaxed_validation_for_class,
    set_strict_validation_for_class
)
from pyonepassword.op_items._op_item_type_registry import OPItemFactory
from pyonepassword.op_items.item_validation_policy import (
    _OPItemValidationPolicy
)


@pytest.fixture(autouse=True)
def init_item_validation_policy():
    relaxed_classes = set(_OPItemValidationPolicy._relaxed_item_classes)
    relaxed_flag = _OPItemValidationPolicy._relaxed_validation

    yield  # clean up after each test

    _OPItemValidationPolicy._relaxed_item_classes = relaxed_classes
    _OPItemValidationPolicy._relaxed_validation = relaxed_flag


def test_relaxed_validation_items_registered_01():
    """
    Verify that all item types registered with OPItemFactory also have a relaxed validation variant
    """
    missing_item_types = []
    for item_type in OPItemFactory._TYPE_REGISTRY.keys():
        if item_type not in OPItemFactory._RELAXED_TYPE_REGISTRY:
            missing_item_types.append(item_type)

    assert len(
        missing_item_types) == 0, f"Missing relaxed validation item types: {missing_item_types}"


def test_global_relaxed_validation_policy_01(non_conformant_data: NonConformantData):
    """
    Test enable_relaxed_validation() global policy

    Verify:
        - relaxed validation policy is enabled globally
        - An OPLoginItem object can be created with non-conformant data
        - After
    """
    login_dict = non_conformant_data.data_for_name("login-duplicate-section")
    enable_relaxed_validation()
    assert get_relaxed_validation()
    assert OPLoginItem(login_dict)


def test_global_relaxed_validation_policy_02(non_conformant_data: NonConformantData):
    """
    Enable then disable global relaxed item validation policy

    Verify:
        - After enabling relaxed validation policy, that it is in fact enabled
        - After disabling relaxed validation policy, that it is in fact disabled
        - an OPLoginItem cannot be created with non-conformant data
    """
    login_dict = non_conformant_data.data_for_name("login-duplicate-section")
    enable_relaxed_validation()
    assert get_relaxed_validation()
    disable_relaxed_validation()
    assert not get_relaxed_validation()
    with pytest.raises(OPSectionCollisionException):
        assert OPLoginItem(login_dict)


def test_item_class_relaxed_validation_01(non_conformant_data: NonConformantData):
    """
    Set relaxed validation policy for the OPLoginItem class

    Verify:
        - Before setting the policy, an OPLoginItem cannot be created with non-conformant data
        - After setting the policy, an OPLoginItem CAN be created with non-conformant data
    """
    login_dict = non_conformant_data.data_for_name("login-field-missing-id")
    with pytest.raises(OPInvalidItemException):
        OPLoginItem(login_dict)
    set_relaxed_validation_for_class(OPLoginItem)
    assert OPLoginItem(login_dict)


def test_item_class_relaxed_validation_02():
    """
    Test removing an item class from relaxed valiation after adding it

    Verify:
        - To start, the OPLoginItem class is not in the per-class relaxed validation policy
        - After adding the OPLoginItem class to the relaxed validation policy, that it is in fact enabled
        - After removing the OPLoginItem class from the relaxed validation policy, that it is no longer enabled
    """
    assert not get_relaxed_validation_for_class(OPLoginItem)
    set_relaxed_validation_for_class(OPLoginItem)
    assert get_relaxed_validation_for_class(OPLoginItem)
    set_strict_validation_for_class(OPLoginItem)
    assert not get_relaxed_validation_for_class(OPLoginItem)


def test_item_class_relaxed_validation_03(non_conformant_data: NonConformantData):
    """
    Test removing an item class from relaxed valiation after adding it

    Verify:
        - After setting the policy, an OPLoginItem can be created with non-conformant data
        - After removing the policy, an OpLoginItem cannot be created with non-conformant data
    """
    login_dict = non_conformant_data.data_for_name("login-field-missing-id")

    # To start with, check relaxed validation is not enabled for OPLoginItem
    assert not get_relaxed_validation_for_class(OPLoginItem)

    # Add OPLoginItem to the per-class relaxed validation list
    set_relaxed_validation_for_class(OPLoginItem)
    # check OPLoginItem can successfully be created
    assert OPLoginItem(login_dict)

    # Remove OPLoginItem from relaxed validation list
    set_strict_validation_for_class(OPLoginItem)
    # verify OPLoginItem can no longer be created from non-conformant data
    with pytest.raises(OPInvalidItemException):
        OPLoginItem(login_dict)
