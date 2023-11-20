from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyonepassword import OP
    from pyonepassword.api.object_types import OPDocumentItem

    from ...fixtures.binary_input_data import BinaryImageData

import pytest

from ...test_support.util import digest

pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


@pytest.mark.usefixtures("setup_stateful_document_edit")
def test_document_edit_01(signed_in_op: OP, binary_image_data: BinaryImageData):
    """
    Test: OP.document_edit() with path to a replacement file
        - Retrieve document bytes and filename via OP.document_get()
        - Call document_edit(), providing the path to a new file to replace the document
        - Retreive the same item a second time
    Verify:
        - The digest of the original document bytes does not match the digest of the replacement document bytes
        - The the original document filename remains unchanged after the edit
        - The edited document's digest matches the digest of the replacement document bytes
    """
    item_name = "example document 01"
    vault = "Test Data 2"
    input_data_path = binary_image_data.data_path_for_name(
        "replacement-image-01")
    input_data = binary_image_data.data_for_name("replacement-image-01")
    input_data_digest = digest(input_data)

    filename_1, data_1 = signed_in_op.document_get(item_name, vault=vault)
    digest_1 = digest(data_1)

    # these should be different, else we've messed up
    # and the document has already been edited
    assert digest_1 != input_data_digest

    # Provide path to the input file
    # we'll test providing input bytes separately
    signed_in_op.document_edit(item_name, input_data_path, vault=vault)

    filename_2, data_2 = signed_in_op.document_get(item_name, vault=vault)
    digest_2 = digest(data_2)

    # filename shouldn't change because we didn't explicitly set it
    assert filename_2 == filename_1
    # The updated document digest should now match the digest of the input file
    assert digest_2 == input_data_digest


@pytest.mark.usefixtures("setup_stateful_document_edit")
def test_document_edit_02(signed_in_op: OP, binary_image_data: BinaryImageData):
    """
    Test: OP.document_edit() with the actual bytes of a replacement file
        - Retrieve document bytes and filename via OP.document_get()
        - Call document_edit(), providing the actual bytes of a new file to replace the document
        - Retreive the same item a second time
    Verify:
        - The digest of the original document bytes does not match the digest of the replacement document bytes
        - The the original document filename remains unchanged after the edit
        - The edited document's digest matches the digest of the replacement document bytes
    """
    item_name = "example document 01"
    vault = "Test Data 2"

    input_data = binary_image_data.data_for_name("replacement-image-01")
    input_data_digest = digest(input_data)

    filename_1, data_1 = signed_in_op.document_get(item_name, vault=vault)
    digest_1 = digest(data_1)

    # these should be different, else we've messed up
    # and the document has already been edited
    assert digest_1 != input_data_digest

    # Provide the literal bytes of the input file
    # we'll test providingthe path to the input file separately
    signed_in_op.document_edit(item_name, input_data, vault=vault)

    filename_2, data_2 = signed_in_op.document_get(item_name, vault=vault)
    digest_2 = digest(data_2)

    # filename shouldn't change because we didn't explicitly set it
    assert filename_2 == filename_1
    # The updated document digest should now match the digest of the input file
    assert digest_2 == input_data_digest


@pytest.mark.usefixtures("setup_stateful_document_edit")
def test_document_edit_03(signed_in_op: OP, binary_image_data: BinaryImageData):
    """
    Test: OP.document_edit() while setting a new item title
        - Retrieve document item via OP.item_get()
        - Call document_edit(), providing the new file path along with a new title
        - Retreive the same item a second time
    Verify:
        - The title of the original document item does not match the new document title
        - The title of the second retrieved item matches the the new document title
    """
    item_name = "example document 02"
    new_item_title = "example document 02 - updated"
    vault = "Test Data 2"

    input_data_path = binary_image_data.data_path_for_name(
        "replacement-image-02")
    document_item_1: OPDocumentItem = signed_in_op.item_get(
        item_name, vault=vault)
    assert document_item_1.title != new_item_title
    # Provide path to the input file
    # we'll test providing input bytes separately
    signed_in_op.document_edit(
        item_name, input_data_path, new_title=new_item_title, vault=vault)

    document_item_2: OPDocumentItem = signed_in_op.item_get(
        new_item_title, vault=vault)
    assert document_item_2.title == new_item_title
