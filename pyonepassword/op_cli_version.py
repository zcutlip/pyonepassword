import re

MAX_BETA_STR = f"{0xffffffff}.{0xffff}.{0xffff}"


class OPCLIVersion:
    def __init__(self, version: str, skip_beta=False):
        if isinstance(version, int):
            version = str(version)
        version, beta_num = self._parse_beta(version)
        version_tuple = version.split(".")
        if not skip_beta:
            self._beta_num = beta_num
        else:
            self._beta_num = -1
        parts = []
        for part in version_tuple:
            parts.append(int(part, 0))
        self._parts = parts

    @property
    def beta_ver(self):
        # if this is not a beta, set beta_ver to an absurdly high value
        # so it beats any actual beta version
        # this will make lt/gt/eq comparison logic simpler
        beta_ver = None
        if self._beta_num is None:
            beta_ver = OPCLIVersion(MAX_BETA_STR, skip_beta=True)
        elif self._beta_num == -1:
            pass
        else:
            beta_ver = OPCLIVersion(self._beta_num, skip_beta=True)
        return beta_ver

    @property
    def is_beta(self) -> bool:
        _is_beta = self._beta_num is not None and self._beta_num >= 0
        return _is_beta

    def _parse_beta(self, version_string):
        regex = r".*(-beta.*)$"
        beta_num = None
        match = re.match(regex, version_string)
        if match:
            beta_string = match.groups()[0]
            version_string = version_string.rstrip(beta_string)
            beta_num = beta_string.lstrip("-beta.")
            beta_num = int(beta_num)
        return version_string, beta_num

    def _normalize(self, other):
        parts_self = list(self._parts)
        parts_other = list(other._parts)

        # be robust about version strings of differing lenghts
        # e.g., 11.3.1 vs 11.3.1.1
        diff_len = len(parts_self) - len(parts_other)

        # if the length difference was negative, _parts_other is longer,
        # and we need to exitend _parts self
        while diff_len < 0:
            parts_self.append(0)
            diff_len += 1
        # if diff was positive, we need to extend _parts other
        while diff_len > 0:
            parts_other.append(0)
            diff_len -= 1

        # appending the OPCLIVersion object for the beta version number
        # will allow it to be transparently compared just like all the other version parts
        # then the lt/gt/eq logic doesn't have to change
        beta_ver = self.beta_ver
        if beta_ver is not None:
            parts_self.append(beta_ver)

        beta_ver = other.beta_ver
        if beta_ver is not None:
            parts_other.append(beta_ver)

        # now 11.3.1 vs 11.3.1.1 becomes
        # 11.3.1.0 vs 11.3.1.1, and can be compared 1 to 1
        return (parts_self, parts_other)

    def __str__(self):
        beta_part = None
        if self.is_beta:
            beta_part = f"-beta.{self._beta_num}"
        _str = ".".join([str(i) for i in self._parts])
        if beta_part:
            _str += beta_part
        return _str

    def __eq__(self, other):
        equal = id(self) == id(other)

        if not equal:
            if not isinstance(other, OPCLIVersion):
                other = OPCLIVersion(other)

            parts_self, parts_other = self._normalize(other)
            equal = True
            for i, part in enumerate(parts_self):
                if part != parts_other[i]:
                    equal = False
                    break

        return equal

    def __ne__(self, other):
        ne = not self.__eq__(other)
        return ne

    def __lt__(self, other):
        if id(self) == id(other):
            return False

        if not isinstance(other, type(self)):
            other = OPCLIVersion(other)

        lt = False
        _parts_self, _parts_other = self._normalize(other)

        for i, part in enumerate(_parts_self):
            if part > _parts_other[i]:
                break
            elif part == _parts_other[i]:
                continue
            elif part < _parts_other[i]:
                lt = True
                break

        return lt

    def __le__(self, other):
        le = self.__lt__(other) or self.__eq__(other)
        return le


MINIMUM_ITEM_CREATION_VERSION = OPCLIVersion('1.12.1')
DOCUMENT_BYTES_BUG_VERSION = OPCLIVersion('2.2.0')
