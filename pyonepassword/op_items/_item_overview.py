import copy


class URLEntry(dict):
    def __init__(self, url_dict):
        ud = copy.deepcopy(url_dict)
        super().__init__(ud)

    @property
    def label(self):
        return self["l"]

    @property
    def url(self):
        return self["u"]
