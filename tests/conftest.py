import pytest

pytest_plugins = [
    "tests.fixtures.op_fixtures"
]


@pytest.fixture(autouse=True)
def reset_class_state():
    from pyonepassword import OP

    # at the moment this just resets OP's CLI version check state
    # multiple test cases in a test module that expect the version check to happen
    # require this because version check is cached based on the `op_path`
    OP._reset_class()
    # not sure if it's necessary to del OP, but since we didn't really want to import it at this point
    # let's go ahead and do it
    del OP
