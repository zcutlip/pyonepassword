"""
Very rarely 'op' will return a non-conformant item where a section dictionary has no "id" field
We need to (optionally) handle those situations gracefully
This module contains test cases for that scenario
"""


from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from ..fixtures.non_comformant_data import NonConformantData
    # from ..fixtures.expected_login import ExpectedLogin, ExpectedLoginItemData

from pyonepassword.api.exceptions import OPInvalidItemException
from pyonepassword.api.object_types import (  # OPServerItemRelaxedValidation
    OPServerItem
)
from pyonepassword.api.validation import set_relaxed_validation_for_class
# from pyonepassword.op_items._op_item_type_registry import OPItemFactory
from pyonepassword.op_items.item_validation_policy import (
    _OPItemValidationPolicy
)

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")

NON_CONFORMANT_ENTRY = "server-section-missing-id"


@pytest.fixture(autouse=True)
def init_item_validation_policy(request):
    relaxed_classes = set(_OPItemValidationPolicy._relaxed_item_classes)
    relaxed_flag = _OPItemValidationPolicy._relaxed_validation

    yield  # clean up after each test

    _OPItemValidationPolicy._relaxed_item_classes = relaxed_classes
    _OPItemValidationPolicy._relaxed_validation = relaxed_flag


def test_item_section_missing_id_01(non_conformant_data: NonConformantData):
    item_json = non_conformant_data.data_for_name(NON_CONFORMANT_ENTRY)
    with pytest.raises(OPInvalidItemException):
        OPServerItem(item_json)


def test_item_section_missing_id_02(non_conformant_data: NonConformantData):
    item_json = non_conformant_data.data_for_name(NON_CONFORMANT_ENTRY)
    set_relaxed_validation_for_class(OPServerItem)
    item = OPServerItem(item_json)
    # TODO: assert item properties
    assert item
