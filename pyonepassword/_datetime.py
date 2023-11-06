import re
from datetime import datetime


def fromisoformat_z(date_string: str) -> datetime:
    """
    Python's datetime.datetime.fromisoformat() can't parse datetime strings
    With a UTC 'Z' timezone suffix instead of +00:00
    And there's no way to do it without an external package like dateutil
    https://bugs.python.org/issue35829
    """

    if date_string.endswith('Z'):
        _str = date_string.rstrip('Z')
        _str += "+00:00"
    elif re.match(r".*[+-]\d{2}:\d{2}$", date_string):
        # We shouldn't ever get this, but we also shouldn't blow up on it,
        # so work with it if it happens
        _str = date_string
    else:
        # Mirror the ValueError that datetime.fromisoformat() raises
        raise ValueError(
            f"Invalid TZ terminated isoformat string: '{date_string}'")
    datetime_obj = datetime.fromisoformat(_str)
    return datetime_obj
