import pytest

from pyonepassword._datetime import fromisoformat_z


def test_datetime_isoformat_no_z_01():
    invalid_date_str = "2021-06-29T18:31:30"
    with pytest.raises(ValueError):
        fromisoformat_z(invalid_date_str)


def test_datetime_isoformat_utc_zterm_01(expected_datetime_data):
    datetime_str = "2021-06-29T18:31:30Z"
    expected_datetime = expected_datetime_data.datetime_for_key(
        "example-datetime")
    result = fromisoformat_z(datetime_str)
    assert result == expected_datetime


def test_datetime_isoformat_utc_zeros_01(expected_datetime_data):
    datetime_str = "2021-06-29T18:31:30+00:00"
    expected_datetime = expected_datetime_data.datetime_for_key(
        "example-datetime")
    result = fromisoformat_z(datetime_str)
    assert result == expected_datetime
