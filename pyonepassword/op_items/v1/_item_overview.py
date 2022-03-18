import copy

from .._op_items_base import URLEntry


class URLEntryV1(URLEntry):

    @property
    def label(self):
        return self["l"]

    @property
    def url(self):
        return self["u"]


class OPItemOverview(dict):

    def __init__(self, overview_dict):
        od = copy.deepcopy(overview_dict)
        super().__init__(od)
        _urls = self._process_urls()
        if _urls is not None:
            self["URLs"] = _urls

    def _process_urls(self):
        # Some item types, namely Login and Password can
        # have a URLs dict in their overview
        # other item types do not. We want to make accessing those
        # transparent, making them available if they exist, but not
        # failing if they don't
        url_items = None
        url_dicts = self.get("URLs", [])
        if url_dicts:
            url_items = []
            for d in url_dicts:
                url = URLEntryV1(d)
                url_items.append(url)
        return url_items

    def url_list(self):
        return self.get("URLs", None)


class OPMutableItemOverview(OPItemOverview):

    def set_url(self, url, label=""):
        url_dict = {
            "l": label,
            "u": url
        }
        # TODO: is it an error if we alread have one or more URLs?
        new_url = URLEntryV1(url_dict)
        self["URLs"] = [new_url]
