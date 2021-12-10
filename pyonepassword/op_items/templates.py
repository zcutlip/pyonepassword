import json
import re

from ..pkg_resources import pkgfiles

from .. import data


class TemplateNotFoundException(Exception):
    def __init__(self, template_id):
        self.template_id = template_id
        msg = f"Template not found for: {template_id:03d}"
        super().__init__(msg)


class TemplateDirectory:
    TEMPLATE_LIST = "template-list.json"

    def __init__(self):
        self._templates = self._template_index()

    def template(self, template_id):
        try:
            template_name = self._templates[template_id]
        except KeyError as e:
            raise TemplateNotFoundException(template_id) from e

        fname = f"{template_name}.json"

        template_obj = self._load_from_json(fname)
        return template_obj

    def _template_index(self):
        template_dict = {}
        template_list = self._load_from_json(self.TEMPLATE_LIST)
        for entry in template_list:
            uuid = entry["uuid"]
            name = entry["name"]
            name = self._normalize_name(name)
            template_dict[uuid] = name

        return template_dict

    def _load_from_json(self, fanme):
        loaded = None
        with pkgfiles(data).joinpath(fanme).open("r") as _file:
            loaded = json.load(_file)

        return loaded

    def _normalize_name(self, name: str):
        name = name.lower()
        name = re.sub(r"\W+", "-", name)
        return name
