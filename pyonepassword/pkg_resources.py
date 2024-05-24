# importlib.resources.files introduced in python 3.9
from importlib.resources import files as pkgfiles  # noqa: F401
from pathlib import Path


def data_location_as_path(package, sub_path) -> Path:
    """
    Convenience function to get a Path object from a package and a subpath
    within the package
    """
    # joinpath() returns a Traversable
    # to turn it into Path we first turn it into a string
    if not isinstance(sub_path, str):
        sub_path = str(sub_path)  # pragma: no coverage
    _data_path = pkgfiles(package).joinpath(sub_path)
    _data_path_str = str(_data_path)
    data_path = Path(_data_path_str)
    return data_path
