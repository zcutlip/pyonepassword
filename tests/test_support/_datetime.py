from datetime import datetime

"""
This is intentially an exact copy of the _datetime module in pyonepassword.
We want to to datetime conversion in test cases without relying on code being tested
"""


def fromisoformat_z(date_string: str) -> datetime:
    """
    Python's datetime.datetime.fromisoformat() can't parse datetime strings
    With a UTC 'Z' timezone suffix instead of +00:00
    And there's no way to do it without an external package like dateutil
    https://bugs.python.org/issue35829
    """
    if not date_string.endswith('Z'):
        # Mirror the ValueError that datetime.fromisoformat() raises
        raise ValueError(
            f"Invalid Z-terminated isoformat string: '{date_string}'")
    _str = date_string.rstrip('Z')
    _str += "+00:00"
    datetime_obj = datetime.fromisoformat(_str)
    return datetime_obj
