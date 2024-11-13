from __future__ import annotations

from typing import TYPE_CHECKING

# import pytest

if TYPE_CHECKING:
    from pyonepassword import OP


def test_item_share_010(signed_in_op: OP):
    item_name = "Example Login Item 22"
    share_url = signed_in_op.item_share(item_name)
    print(share_url)
