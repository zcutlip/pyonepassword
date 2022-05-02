from typing import List, Union

from .json import safe_unjson


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
    def account_uuid(self) -> str:
        return self["account_uuid"]

    @property
    def shorthand(self) -> Union[str, None]:
        return self.get("shorthand")


class OPAccountList(List[OPAccount]):

    def __init__(self, account_list_or_json):
        super().__init__()
        account_list = safe_unjson(account_list_or_json)
        for account_dict in account_list:
            op_account = OPAccount(account_dict)
            self.append(op_account)

    def account_for_email(self, email: str):
        acct = None
        for account in self:
            if account.email == email:
                acct = account
                break
        return acct
