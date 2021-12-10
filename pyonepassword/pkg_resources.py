try:
    from importlib.resources import files as pkgfiles  # noqa: F401
except ImportError:
    from importlib_resources import resources as pkgresources  # noqa: F401
