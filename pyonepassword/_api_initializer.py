# Most of the object types and descriptor types need to
# register themselves with a factory class
# so we need to import them here to ensure that happens
from .api.decorators import *  # noqa: F401, F403
from .api.descriptor_types import *  # noqa: F401, F403
from .api.object_types import *  # noqa: F401, F403

# Declare token object that can be imported into __init__.py without polluting namespace
# to ensure the classes mentioned above get imported & initialized
_API_INITIALIZED = True
