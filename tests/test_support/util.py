import re
from hashlib import sha256


def digest(data):
    digest = sha256(data)
    digest_str = digest.hexdigest()
    return digest_str


def is_uuid(id_str: str):
    """
    This is a copy of the is_uuid() function in pyonepassword.uuid
    We want to use it to verify UUIDs without relying on code being tested
    """
    b32_regex = r'^[A-Z0-9]{26}$'
    b32_lowercase_regex = r'^[a-z0-9]{26}$'
    hex_bytes_regex = r'[a-zA-Z0-9]{32}$'
    section_id_regex = r'Section_[a-zA-Z0-9]{32}$'

    match = False
    for regex in [b32_regex, b32_lowercase_regex, hex_bytes_regex, section_id_regex]:
        if re.match(regex, id_str):
            match = True
            break

    return match
