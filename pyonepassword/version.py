from . import __summary__, __title__, __version__


class PyonepasswordAbout:

    def __str__(self):
        return "%s %s version %s" % (__title__, __summary__, __version__)
