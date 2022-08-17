import base64
import random
import re


class OPUniqueIdentifierBase32:
    BYTE_COUNT = 16

    def __init__(self, uppercase=False):
        self._random_bytes = random.randbytes(self.BYTE_COUNT)
        self._upper = uppercase

    def __str__(self):
        unique_id_bytes = self._random_bytes
        b32unique_id = base64.b32encode(unique_id_bytes)
        b32unique_id = b32unique_id.decode("utf-8")
        b32unique_id = b32unique_id.rstrip('=')
        if not self._upper:
            b32unique_id = b32unique_id.lower()
        return b32unique_id


class OPUniqueIdentifierHex(OPUniqueIdentifierBase32):
    PREFIX = ""

    def __init__(self, uppercase=True):
        super().__init__(uppercase=uppercase)

    def __str__(self):
        unique_id_bytes = self._random_bytes
        unique_id = unique_id_bytes.hex()
        if self._upper:
            unique_id = unique_id.upper()
        unique_id = f"{self.PREFIX}{unique_id}"
        return unique_id


class OPUniqueSectionIdentifier(OPUniqueIdentifierHex):
    PREFIX = "Section_"


def is_uuid(id_str: str):
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
