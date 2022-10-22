try:
    # register colored_traceback hook if in a dev environment (dev-reqs.txt)
    import colored_traceback.auto
except ImportError:  # pragma: no coverage
    # otherwise just stick to the basics
    pass

from .__about__ import __summary__, __title__, __version__
# Import and discard _API_INITIALIZER to ensure all API classes get registered
from ._api_initializer import _API_INITIALIZED as _
from .pyonepassword import OP
