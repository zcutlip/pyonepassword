import pytest

from pyonepassword import OP, OPNotFoundException


def test_missing_op():
    with pytest.raises(OPNotFoundException):
        OP(op_path="no-such-op")
