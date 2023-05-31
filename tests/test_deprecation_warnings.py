import warnings


def test_api_deprecation_01():
    """
    Import deprecated OPNotSignedInException class from
    pyonepassword.api.exceptions

    Ensure there is a deprecation warning
    """
    with warnings.catch_warnings(record=True) as warning_list:
        from pyonepassword.api.exceptions import \
            OPNotSignedInException  # noqa: F401
        assert warning_list


def test_api_deprecation_02():
    """
    Import deprecated OPNotSignedInException class from
    pyonepassword.py_op_exceptions

    Ensure there is a deprecation warning
    """
    with warnings.catch_warnings(record=True) as warning_list:
        from pyonepassword.py_op_exceptions import \
            OPNotSignedInException  # noqa: F401
        assert warning_list
