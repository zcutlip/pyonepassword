"""
Very rarely 'op' will return a non-conformant item where there are duplicate field
dictionaries, including the "unique" field ID

This results in a conflict in two possible ways:

1. creating all the field objects and adding them to the map of field IDs
2. Even if (1) is handled, there's the issue of registering the same field
   twice with a given section

We need to (optionally) handle those situations gracefully
This module contains test cases for that scenario
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.non_comformant_data import NonConformantData
    # from ..fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

from pyonepassword.api.exceptions import OPItemFieldCollisionException
from pyonepassword.api.object_types import (
    OPLoginItem,
    OPLoginItemRelaxedValidation
)

NON_CONFORMANT_ENTRY = "login-duplicate-field"
EXPECTED_LOGIN_DATA = ""


def test_login_duplicate_fields_01(non_conformant_data: NonConformantData):
    login_json = non_conformant_data.data_for_name(NON_CONFORMANT_ENTRY)
    with pytest.raises(OPItemFieldCollisionException):
        OPLoginItem(login_json)


def test_login_duplicate_fields_02(non_conformant_data: NonConformantData):
    login_json = non_conformant_data.data_for_name(NON_CONFORMANT_ENTRY)
    OPLoginItemRelaxedValidation(login_json)
