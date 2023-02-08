import os
import platform


def is_windows():
    return platform.system() == 'Windows'


HOME_ENV_VAR = 'HOME'

if is_windows():
    HOME_ENV_VAR = 'USERPROFILE'

DEV_NULL = os.devnull
