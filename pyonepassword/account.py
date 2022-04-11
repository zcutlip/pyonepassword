import json

from typing import Union


class OPAccount(dict):

    @property
    def url(self) -> str:
        return self["url"]

    @property
    def email(self) -> str:
        return self["email"]

    @property
    def user_uuid(self) -> str:
        return self["user_uuid"]

    @property
    def shorthand(self) -> Union[str, None]:
        return self.get("shorthand")


class OPAccountList(list):

    def __init__(self, account_list):
        super().__init__()
        if isinstance(account_list, str):
            account_list = json.loads(account_list)
        for account_dict in account_list:
            op_account = OPAccount(account_dict)
            self.append(op_account)
