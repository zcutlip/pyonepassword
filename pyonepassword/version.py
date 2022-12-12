from . import __summary__, __title__, __version__


class PyOPAbout:
    def __init__(self) -> None:
        self.version = __version__
        self.summary = __summary__
        self.title = __title__

    def __str__(self):
        return f"{self.title.upper()}: {self.summary}. Version {self.version}"


class PyOPAboutMixin:
    _about = PyOPAbout()

    @classmethod
    @property
    def about(cls) -> str:
        return str(cls._about)

    @classmethod
    @property
    def version(cls) -> str:
        return cls._about.version
