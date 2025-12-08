import json
import re
import warnings

from . import data
from .pkg_resources import data_location_as_path
from .py_op_exceptions import OPBaseException

MAX_BETA_STR = f"{0xffffffff}.{0xffff}.{0xffff}"


class OPCLIVersionSupportException(OPBaseException):
    def __init__(self, version):
        msg = f"op version not supported: {version}"
        super().__init__(msg)


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
    def major(self) -> int:
        return self._parts[0]

    @property
    def minor(self) -> int:
        return self._parts[1]

    @property
    def patch(self):
        return self._parts[2]

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
            # get "-beta.01"
            beta_string = match.groups()[0]
            # strip -beta.01 from the end of version_string, leaving "2.18.0"
            version_string = re.sub(beta_string, '', version_string)
            # extract '01' from '-beta.01'
            beta_num = beta_string.split(".")[1]
            # convert beta num to an int
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
            beta_part = f"-beta.{self._beta_num:02d}"
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

        if not isinstance(other, OPCLIVersion):
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

    def __gt__(self, other):
        gt = not self.__le__(other)
        return gt

    def __ge__(self, other):
        ge = self.__eq__(other) or self.__gt__(other)
        return ge


class OPVersionSupport:
    _VERSION_SUPPORT_KEY = "version-support"
    _VERSION_SUPPORTED_KEY = "supported"
    _VERSION_MINIMUM_KEY = "minimum"
    _FEATURE_SUPPORT_KEY = "feature-support"
    _BUG_FIXES_KEY = "bug-fixes"

    def __init__(self):
        data_path = data_location_as_path(data, data.OP_VERSION_SUPPORT)
        support_dict = json.load(open(data_path, "r"))
        self._version_support = support_dict
        self._populate_version_objects()

    def _populate_version_objects(self):
        ver_str = self.supported_version
        ver = OPCLIVersion(ver_str)
        self._set_supported_version(ver)

        ver_str = self.minimum_version
        ver = OPCLIVersion(ver_str)
        self._set_minimum_version(ver)

    def _set_version_support(self, key, version):
        vs = self.version_support()
        vs[key] = version

    def _set_supported_version(self, version):
        self._set_version_support(self._VERSION_SUPPORTED_KEY, version)

    def _set_minimum_version(self, version):
        self._set_version_support(self._VERSION_MINIMUM_KEY, version)

    @property
    def minimum_version(self) -> str:
        vs = self.version_support()
        dv = vs[self._VERSION_MINIMUM_KEY]
        return dv

    @property
    def supported_version(self):
        vs = self.version_support()
        dv = vs[self._VERSION_SUPPORTED_KEY]
        return dv

    def version_support(self):
        return self._version_support[self._VERSION_SUPPORT_KEY]

    def _feature_support(self):  # pragma: no cover
        return self._version_support[self._FEATURE_SUPPORT_KEY]

    def _bug_fix_versions(self):  # pragma: no cover
        return self._version_support[self._BUG_FIXES_KEY]

    def check_version_support(self, op_version) -> bool:
        if not isinstance(op_version, OPCLIVersion):
            op_version = OPCLIVersion(op_version)

        min_ver = self.minimum_version
        supported_ver = self.supported_version
        if op_version < min_ver:
            raise OPCLIVersionSupportException(op_version)

        if op_version < supported_ver:
            msg = f"op version is deprecated: {op_version}"
            warnings.warn(msg, category=DeprecationWarning)

        return True
