# __future__.annotaitons, and typing.TYPE_CHECKING
# enable anything imported for type hinting to disappear at run time
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

# make imports for type-hinting disappear at run-time to avoid
# circular imports.
# this also reduced exercising tested code simply by importing
if TYPE_CHECKING:
    from ..fixtures.expected_server import ExpectedServerItemData
    from ..fixtures.valid_data import ValidData

from pyonepassword.api.object_types import OPServerItem

# ensure HOME env variable is set, and there's a valid op config present
pytestmark = pytest.mark.usefixtures("valid_op_cli_config_homedir")


def test_server_item_010(valid_data: ValidData, expected_server_data: ExpectedServerItemData):

    server_name = "Example Server"

    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.username == expected.username


def test_server_item_020(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    server_name = "Example Server"

    item_dict = valid_data.data_for_name("example-server-1")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.password == expected.password


def test_server_item_030(valid_data: ValidData):
    item_dict = valid_data.data_for_name("example-server-1")

    result = OPServerItem(item_dict)
    assert result.url is None


def test_server_item_040(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    server_name = "Example Server 2"

    item_dict = valid_data.data_for_name("example-server-2")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.url == expected.url


def test_server_item_050(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    server_name = "Example Server 2"

    item_dict = valid_data.data_for_name("example-server-2")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.admin_console_username == expected.admin_console_username


def test_server_item_060(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    server_name = "Example Server 2"

    item_dict = valid_data.data_for_name("example-server-2")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)
    assert result.admin_console_password == expected.admin_console_password


def test_server_item_070(valid_data: ValidData, expected_server_data: ExpectedServerItemData):
    server_name = "Example Server 2"

    item_dict = valid_data.data_for_name("example-server-2")
    expected = expected_server_data.data_for_server(server_name)

    result = OPServerItem(item_dict)

    assert result.admin_console_url == expected.admin_console_url
