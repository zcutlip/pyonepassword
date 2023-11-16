from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyonepassword import OP

    from ...fixtures.binary_input_data import BinaryImageData

import pytest

from ...test_support.util import digest

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_document_edit")
def test_document_edit_01(signed_in_op: OP, binary_image_data: BinaryImageData):
    item_name = "example document 01"
    vault = "Test Data 2"
    input_data_path = binary_image_data.data_path_for_name(
        "replacement-image-01")
    input_data = binary_image_data.data_for_name("replacement-image-01")
    input_data_digest = digest(input_data)

    filename_1, data_1 = signed_in_op.document_get(item_name, vault=vault)
    digest_1 = digest(data_1)

    assert digest_1 != input_data_digest
    signed_in_op.document_edit(item_name, input_data_path, vault=vault)

    filename_2, data_2 = signed_in_op.document_get(item_name, vault=vault)
    digest_2 = digest(data_2)

    # filename shouldn't change because we didn't explicitly set it
    assert filename_2 == filename_1
    assert digest_2 == input_data_digest
