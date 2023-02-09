"""
Fairly often, 1Password will return items where one or more field IDs is an empty string.
If there are more than one "empty string" field IDS, this results in field ID collisions.

We need to (optionally) handle those situations gracefully
This module contains test cases for that scenario
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.non_comformant_data import NonConformantData
    from ..fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

from pyonepassword.api.exceptions import OPInvalidItemException
from pyonepassword.api.object_types import (
    OPLoginItem,
    OPLoginItemRelaxedValidation
)
# from pyonepassword.op_items._op_item_type_registry import OPItemFactory
from pyonepassword.op_items.item_validation_policy import (
    _OPItemValidationPolicy
)

NON_CONFORMANT_ENTRY = "login-field-missing-id"
EXPECTED_LOGIN_DATA = "Login Item with Field missing ID"


@pytest.fixture(autouse=True)
def init_item_validation_policy(request):
    relaxed_classes = set(_OPItemValidationPolicy._relaxed_item_classes)
    relaxed_flag = _OPItemValidationPolicy._relaxed_validation

    yield  # clean up after each test

    _OPItemValidationPolicy._relaxed_item_classes = relaxed_classes
    _OPItemValidationPolicy._relaxed_validation = relaxed_flag


def test_field_missing_id_01(non_conformant_data: NonConformantData):
    item_json = non_conformant_data.data_for_name(NON_CONFORMANT_ENTRY)
    with pytest.raises(OPInvalidItemException):
        OPLoginItem(item_json)


def test_field_missing_id_02(non_conformant_data: NonConformantData,
                             expected_login_item_data: ExpectedLoginItemData):
    expected_login: ExpectedLogin = expected_login_item_data.data_for_login(
        EXPECTED_LOGIN_DATA)
    login_json = non_conformant_data.data_for_name(NON_CONFORMANT_ENTRY)
    login_item = OPLoginItemRelaxedValidation(login_json)

    # we can't do any field except for password, because the rest have empty string IDs
    assert login_item.password == expected_login.password
