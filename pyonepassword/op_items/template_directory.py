import json

from .. import data
from ..pkg_resources import pkgfiles


class OPTemplateDirectory:

    def __init__(self):
        with pkgfiles(data).joinpath(data.TEMPLATE_REGISTRY_JSON).open("r") as _file:
            self._registry = json.load(_file)

    def template_for_category(self, category: str):
        template_name = self._registry[category]
        template = None
        with pkgfiles(data).joinpath(template_name).open("r") as _file:
            template = json.load(_file)

        return template
