from typing import List, Union

from .json import safe_unjson


class OPAccount(dict):
    def __init__(self, account_dict_or_json):
        account_dict = safe_unjson(account_dict_or_json)
        super().__init__(account_dict)

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

    # TODO: Not sure what to do here
    # the 'op whoami' dicts when signed in normally
    # vs. when using a service account
    # are really different
    # but neither self-describe (e.g. with an account type or similar)
    # so for now, just check if this has a ServiceAccountType key
    def is_service_account(self) -> bool:
        svc_acct = False
        if self.get("ServiceAccountType"):
            svc_acct = True
        return svc_acct


class OPAccountList(List[OPAccount]):

    def __init__(self, account_list_or_json):
        super().__init__()
        account_list = safe_unjson(account_list_or_json)
        for account_dict in account_list:
            op_account = OPAccount(account_dict)
            self.append(op_account)

    def account_for_identifier(self, account_id: str):
        acct = None
        for account in self:
            if account_id in [account.account_uuid, account.user_uuid, account.shorthand, account.email, account.url]:
                acct = account
                break
        return acct

    def user_id_for_account_identifier(self, account_id: str):
        user_id = None
        acct = self.account_for_identifier(account_id)
        if acct:
            user_id = acct.user_uuid
        return user_id
