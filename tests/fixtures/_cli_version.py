import json

from pyonepassword import data
from pyonepassword._op_cli_version import OPCLIVersion
from pyonepassword.pkg_resources import data_location_as_path


class OPCLIVersionTesting(OPCLIVersion):

    def decremented(self):
        # 2.23.1 -> 2.22.1
        # major = 2
        # minor = 23
        # patch = 1

        # if minor is >=1, decrement minor & set patch = 0
        # else if patch >=1, then decrement patch
        # else raise exception
        major = self.major
        minor = self.minor
        patch = self.patch
        if minor < 1:
            if patch < 1:
                raise Exception(
                    "minor and patch are zero and can't be deprecated")
            patch = patch - 1
        else:
            minor = minor - 1
            patch = 0

        new_ver_str = f"{major}.{minor}.{patch}"
        new_ver = self.__class__(new_ver_str)
        return new_ver


class _CLIVersionSupportTesting:
    """
    Minimal reimplemenation of OPVersionSupport in order to not depend
    on the thing we're testing
    """
    _VERSION_SUPPORT_KEY = "version-support"
    _VERSION_SUPPORTED_KEY = "supported"
    _VERSION_MINIMUM_KEY = "minimum"

    def __init__(self):
        data_path = data_location_as_path(data, data.OP_VERSION_SUPPORT)
        support_dict = json.load(open(data_path, "r"))
        self._version_support_data = support_dict

    def supported_version(self) -> str:
        supported = self._version_support()[self._VERSION_SUPPORTED_KEY]
        return supported

    def minimum_version(self) -> str:
        minimum_version = self._version_support()[self._VERSION_MINIMUM_KEY]
        return minimum_version

    def _version_support(self) -> str:
        return self._version_support_data[self._VERSION_SUPPORT_KEY]


def _deprecated_version_obj():
    version_support = _CLIVersionSupportTesting()
    version_str = version_support.supported_version()
    ver = OPCLIVersionTesting(version_str)
    ver = ver.decremented()
    return ver


def _deprecated_version_str():
    deprecated_ver = _deprecated_version_obj()
    ver = str(deprecated_ver)
    return ver


def _unsupported_version_obj():
    version_support = _CLIVersionSupportTesting()
    min_ver_str = version_support.minimum_version()
    min_ver = OPCLIVersionTesting(min_ver_str)

    unsupported_ver = min_ver.decremented()
    return unsupported_ver


def _unsupported_version_str():
    unsupported = _unsupported_version_obj()
    unsupported_str = str(unsupported)
    return unsupported_str
