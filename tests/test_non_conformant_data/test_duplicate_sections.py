"""
Very rarely 'op' will return a non-conformant item where there are duplicate section
dictionaries, including the "unique" section ID

We need to (optionally) handle those situations gracefully
This module contains test cases for that scenario
"""


from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.non_comformant_data import NonConformantData
    from ..fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

from pyonepassword.api.exceptions import OPSectionCollisionException
from pyonepassword.api.object_types import (
    OPLoginItem,
    OPLoginItemRelaxedValidation
)
from pyonepassword.api.validation import (
    disable_relaxed_validation,
    enable_relaxed_validation,
    get_relaxed_validation,
    get_relaxed_validation_for_class,
    set_relaxed_validation_for_class
)
from pyonepassword.op_items._op_item_type_registry import OPItemFactory
from pyonepassword.op_items.item_validation_policy import (
    _OPItemValidationPolicy
)

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.fixture(autouse=True)
def init_item_validation_policy():
    relaxed_classes = set(_OPItemValidationPolicy._relaxed_item_classes)
    relaxed_flag = _OPItemValidationPolicy._relaxed_validation

    yield  # clean up after each test

    _OPItemValidationPolicy._relaxed_item_classes = relaxed_classes
    _OPItemValidationPolicy._relaxed_validation = relaxed_flag


def test_login_duplicate_sections_01(non_conformant_data: NonConformantData):
    login_json = non_conformant_data.data_for_name("login-duplicate-section")
    with pytest.raises(OPSectionCollisionException):
        OPLoginItem(login_json)


def test_login_duplicate_sections_02(non_conformant_data: NonConformantData, expected_login_item_data: ExpectedLoginItemData):
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        "Login Item Duplicate Sections")
    login_json = non_conformant_data.data_for_name("login-duplicate-section")
    login_item = OPLoginItemRelaxedValidation(login_json)

    assert login_item.username == expected_login.username


def test_login_duplicate_sections_03(non_conformant_data: NonConformantData, expected_login_item_data: ExpectedLoginItemData):
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        "Login Item Duplicate Sections")
    login_json = non_conformant_data.data_for_name("login-duplicate-section")
    enable_relaxed_validation()
    assert get_relaxed_validation(item_class=OPLoginItem)
    login_item = OPLoginItem(login_json)

    assert login_item.password == expected_login.password


def test_login_duplicate_sections_04(non_conformant_data: NonConformantData, expected_login_item_data: ExpectedLoginItemData):
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        "Login Item Duplicate Sections")
    login_json = non_conformant_data.data_for_name("login-duplicate-section")
    set_relaxed_validation_for_class(OPLoginItem)
    assert get_relaxed_validation(item_class=OPLoginItem)
    login_item = OPLoginItem(login_json)

    assert login_item.created_at == expected_login.created_at


def test_login_duplicate_sections_05(non_conformant_data: NonConformantData, expected_login_item_data: ExpectedLoginItemData):
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        "Login Item Duplicate Sections")
    login_json = non_conformant_data.data_for_name("login-duplicate-section")

    assert get_relaxed_validation_for_class(
        OPLoginItem) is not True
    login_item = OPLoginItemRelaxedValidation(login_json)

    assert login_item.last_edited_by == expected_login.last_edited_by


def test_login_duplicate_sections_06(non_conformant_data: NonConformantData, expected_login_item_data: ExpectedLoginItemData):
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        "Login Item Duplicate Sections")
    login_json = non_conformant_data.data_for_name("login-duplicate-section")

    assert not get_relaxed_validation_for_class(OPLoginItem)
    login_item = OPItemFactory.op_item(login_json, relaxed_validation=True)

    assert isinstance(login_item, OPLoginItem)
    assert login_item.last_edited_by == expected_login.last_edited_by


def test_login_duplicate_sections_07(non_conformant_data: NonConformantData):

    login_json = non_conformant_data.data_for_name("login-duplicate-section")

    assert not get_relaxed_validation_for_class(OPLoginItem)
    OPItemFactory.op_item(login_json, relaxed_validation=True)
    with pytest.raises(OPSectionCollisionException):
        OPItemFactory.op_item(login_json)


def test_login_duplicate_sections_08(non_conformant_data: NonConformantData):
    login_json = non_conformant_data.data_for_name("login-duplicate-section")
    enable_relaxed_validation()
    assert get_relaxed_validation(item_class=OPLoginItem)
    assert OPLoginItem(login_json)
    disable_relaxed_validation()

    assert not get_relaxed_validation(item_class=OPLoginItem)
    with pytest.raises(OPSectionCollisionException):
        assert OPLoginItem(login_json)
