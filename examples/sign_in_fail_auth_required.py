"""
An example of signing in with existing authentication required but not existing

Demonstrates OPAuthenticationException
"""

from do_signin import do_signin

from pyonepassword import OP, logging
from pyonepassword.api.authentication import EXISTING_AUTH_REQD
from pyonepassword.api.exceptions import OPAuthenticationException

if __name__ == "__main__":
    import inspect
    print(__name__)
    print(inspect.getfile(OP))
    logger = logging.console_logger("example-sign-in", level=logging.DEBUG)
    try:
        # ensure OP() fails if there's no existing authentication
        op = do_signin(existing_auth=EXISTING_AUTH_REQD, logger=logger)

    except OPAuthenticationException as e:
        print(e)
