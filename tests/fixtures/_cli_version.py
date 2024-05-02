from pyonepassword._op_cli_version import OPCLIVersion, OPVersionSupport


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


def _deprecated_version_obj():
    version_support = OPVersionSupport()
    ver = version_support.deprecated_version
    return ver


def _deprecated_version_str():
    version_support = OPVersionSupport()
    ver = str(version_support.deprecated_version)
    return ver


def _unsupported_version_obj():
    version_support = OPVersionSupport()
    min_ver_str = str(version_support.minimum_version)
    min_ver = OPCLIVersionTesting(min_ver_str)

    unsupported_ver = min_ver.decremented()

    return unsupported_ver


def _unsupported_version_str():
    unsupported = _unsupported_version_obj()
    unsupported_str = str(unsupported)
    return unsupported_str
