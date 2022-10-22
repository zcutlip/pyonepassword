try:
    from importlib.resources import files as pkgfiles  # noqa: F401
except ImportError:  # pragma: no coverage
    from importlib_resources import files as pkgfiles  # noqa: F401
