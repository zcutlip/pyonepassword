# __future__.annotaitons, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from ..fixtures.expected_server import ExpectedServer, ExpectedServerItemData
    from pyonepassword import OP

from pyonepassword.api.object_types import OPServerItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_admin_user_01(signed_in_op: OP, expected_server_data: ExpectedServerItemData):
    # get item "Example Login 1" --vault "Test Data"
    server_name = "Example Server"
    vault = "Test Data"
    expected: ExpectedServer
    result: OPServerItem
    expected = expected_server_data.data_for_server(
        server_name)
    result = signed_in_op.item_get(server_name, vault=vault)
    assert result.username == expected.username


def test_admin_password_01(signed_in_op: OP, expected_server_data: ExpectedServerItemData):
    server_name = "Example Server"
    vault = "Test Data"
    expected: ExpectedServer
    result: OPServerItem

    expected = expected_server_data.data_for_server(server_name)
    result = signed_in_op.item_get(server_name, vault=vault)
    assert result.password == expected.password


def test_server_url_01(signed_in_op: OP, expected_server_data: ExpectedServerItemData):
    server_name = "Example Server"
    vault = "Test Data"
    result: OPServerItem

    result = signed_in_op.item_get(server_name, vault=vault)
    assert isinstance(result, OPServerItem)
    assert result.url is None


def test_server_url_02(signed_in_op: OP, expected_server_data: ExpectedServerItemData):
    server_id = "3wcd3zsps7fvij47fef6scznxq"
    result: OPServerItem
    expected: ExpectedServer
    expected = expected_server_data.data_for_server(server_id)
    result = signed_in_op.item_get(server_id)
    assert isinstance(result, OPServerItem)
    assert result.url == expected.url


def test_server_admin_console_01(signed_in_op: OP, expected_server_data: ExpectedServerItemData):
    expected: ExpectedServer
    result: OPServerItem
    server_name = "Example Server 2"

    expected = expected_server_data.data_for_server(server_name)

    result = signed_in_op.item_get(server_name, vault="Test Data")

    assert isinstance(result, OPServerItem)
    assert result.admin_console_username == expected.admin_console_username


def test_server_admin_console_02(signed_in_op: OP, expected_server_data: ExpectedServerItemData):
    expected: ExpectedServer
    result: OPServerItem
    server_name = "Example Server 2"

    expected = expected_server_data.data_for_server(server_name)

    result = signed_in_op.item_get(server_name, vault="Test Data")

    assert isinstance(result, OPServerItem)
    assert result.admin_console_password == expected.admin_console_password


def test_server_get_url_field_01(signed_in_op: OP, expected_server_data: ExpectedServerItemData):
    expected: ExpectedServer
    result: OPServerItem
    server_name = "Example Server 2"

    expected = expected_server_data.data_for_server(server_name)

    result = signed_in_op.item_get(server_name, vault="Test Data")

    assert isinstance(result, OPServerItem)
    assert result.admin_console_url is not None
    assert result.admin_console_url == expected.admin_console_url
