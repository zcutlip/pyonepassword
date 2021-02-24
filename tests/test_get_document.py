from typing import Dict
from pyonepassword import OP
from .test_support.util import digest
from .fixtures.expected_data import ExpectedData

def _lookup_item_data(data: ExpectedData, item_id: str) -> Dict:
    item = data.lookup_document(item_id)
    return item


def test_get_document_01(signed_in_op: OP, expected_data):
    item_name = "Example Login 2 - 1200px-SpongeBob_SquarePants_character.svg.png.webp"
    vault = "Test Data"
    expected = _lookup_item_data(expected_data, item_name)
    filename, data = signed_in_op.get_document(item_name, vault=vault)
    sha256_digest = digest(data)
    assert filename == expected["filename"]
    assert len(data) == expected["size"]
    assert sha256_digest == expected["digest"]
