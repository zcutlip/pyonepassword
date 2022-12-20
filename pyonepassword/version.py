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
    def about(cls) -> str:
        """
        Class method to generate an "about" summary string for pyonepassword, which includes:
            - project title
            - project summary
            - project version

        Returns
        -------
        str
            The about string
        """
        return str(cls._about)

    @classmethod
    def version(cls) -> str:
        """
        Class method to return the version string for pyonepassword, e.g., 3.4.0

        Returns
        -------
        str
            The version string
        """
        return cls._about.version
