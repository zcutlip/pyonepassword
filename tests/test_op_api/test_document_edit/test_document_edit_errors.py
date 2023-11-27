from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyonepassword import OP
    from ...fixtures.binary_input_data import BinaryImageData

import pytest

from pyonepassword.api.exceptions import OPDocumentEditException


@pytest.mark.usefixtures("valid_op_cli_config_homedir")
def test_document_edit_invalid_document_01(signed_in_op: OP,
                                           binary_image_data: BinaryImageData):
    document_name = "Invalid Document"
    input_data_path = binary_image_data.data_path_for_name(
        "replacement-image-01")
    with pytest.raises(OPDocumentEditException):
        signed_in_op.document_edit(document_name, input_data_path)
