from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedLoginURL:
    def __init__(self, url_dict):
        self.href = url_dict["href"]
        self.label = url_dict.get("label")
        self.primary = url_dict.get("primary", False)


class ExpectedLogin(ExpectedItemBase):

    def __init__(self, item_dict):
        super().__init__(item_dict)
        url_list = self._data.get("urls", [])
        urls = []
        for url_dict in url_list:
            url = ExpectedLoginURL(url_dict)
            urls.append(url)
        self._urls = urls

    @property
    def username(self) -> str:
        return self._data["username"]

    @property
    def password(self) -> str:
        password = None
        try:
            self._data["password"]
        except KeyError:
            # some expected data objects may not have a "password" key
            # but may have a passsword field dictionary
            password_field = self.field_by_id("password")
            password = password_field.value
        return password

    @property
    def urls(self):
        return self._urls

    @property
    def primary_url(self):
        primary = None
        for url in self._urls:
            if url.primary:
                primary = url
                break
        return primary


class ExpectedLoginItemData(ExpectedItemData):

    def data_for_login(self, login_identifier, version=0) -> ExpectedLogin:
        item_dict = self.data_for_name(login_identifier, version=version)
        login_item = ExpectedLogin(item_dict)
        return login_item
