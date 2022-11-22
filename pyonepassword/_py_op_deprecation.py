
import functools
import warnings
from typing import Any, Callable, Dict

"""
Adapted from:
https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/utils/deprecation.py
"""


class deprecated:  # pragma: no cover

    def __init__(self, extra=""):
        self.extra = extra

    def __call__(self, obj):
        if isinstance(obj, type):
            return self._decorate_class(obj)
        else:
            return self._decorate_fun(obj)

    def _decorate_class(self, cls):
        msg = "Class {} is deprecated".format(cls.__name__)
        if self.extra:
            msg += ": {}".format(self.extra)

        init = cls.__init__

        def wrapped(*args, **kwargs):
            warnings.warn(msg, category=FutureWarning)
            return init(*args, **kwargs)
        cls.__init__ = wrapped

        wrapped.__name__ = '__init__'
        wrapped.__doc__ = self._update_doc(init.__doc__)

        # mypy doesn't like wrapped.deprecated_original = init
        setattr(wrapped, "deprecated_original", init)

        return cls

    def _decorate_fun(self, fun):
        """Decorate function fun"""

        msg = "Function %s is deprecated" % fun.__name__
        if self.extra:
            msg += "; %s" % self.extra

        @functools.wraps(fun)
        def wrapped(*args, **kwargs):
            warnings.warn(msg, category=FutureWarning)
            return fun(*args, **kwargs)

        wrapped.__doc__ = self._update_doc(wrapped.__doc__)

        return wrapped

    def _update_doc(self, olddoc):
        newdoc = "DEPRECATED"
        if self.extra:
            newdoc = "%s: %s" % (newdoc, self.extra)
        if olddoc:
            newdoc = "%s\n\n    %s" % (newdoc, olddoc)
        return newdoc


def deprecated_kwargs(**kwarg_aliases: str) -> Callable:
    """Decorator for deprecated function and method arguments.

    Use as follows:

    @deprecated_kwargs(old_arg='new_arg')
    def myfunc(new_arg):
        ...
    https://stackoverflow.com/a/49802489/17391340
    """

    def deco(f: Callable):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            _rename_kwargs(f.__name__, kwargs, kwarg_aliases)
            return f(*args, **kwargs)

        return wrapper

    return deco


def _rename_kwargs(func_name: str, kwargs: Dict[str, Any], kwarg_aliases: Dict[str, str]):  # pragma: no cover
    """Helper function for deprecating function arguments."""
    for old_kwarg, new_kwarg in kwarg_aliases.items():
        if old_kwarg in kwargs:
            if new_kwarg in kwargs:
                raise TypeError(
                    f"{func_name} received both {old_kwarg} and {new_kwarg} as arguments!"
                    f" {old_kwarg} is deprecated, use {new_kwarg} instead."
                )
            warnings.warn(
                message=(
                    f"`{old_kwarg}` is deprecated as an argument to `{func_name}`; use"
                    f" `{new_kwarg}` instead."
                ),
                category=FutureWarning,
                stacklevel=3,
            )
            kwargs[new_kwarg] = kwargs.pop(old_kwarg)
