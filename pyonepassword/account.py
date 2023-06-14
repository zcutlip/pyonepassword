import os
from typing import List, Union

from .json import safe_unjson

USER_UUID_UNMASK_ENV_VAR = "PYOP_UNMASK_USER_UUID"


class OPAccount(dict):

    # portion of unique IDs to leave unmasked
    UNMASK_LEN = 5

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
            svc_acct = True  # pragma: no coverage
        return svc_acct

    @property
    def sanitized_user_uuid(self) -> str:
        _uuid = self.user_uuid
        if os.environ.get(USER_UUID_UNMASK_ENV_VAR, "0") != "1":
            _uuid = self._sanitized_uuid(_uuid)
        return _uuid

    def _sanitized_uuid(self, uuid_str: str) -> str:
        # This aims to turn:
        # 5GHHPJK5HZC5BAT7WDUXW57G44 into
        # *********************57G44

        if len(uuid_str) <= self.UNMASK_LEN:
            # the thing is too short, so replace everything
            uuid_str = "*" * len(uuid_str)
        else:
            # get the length of the portion we're trying to mask
            star_count = len(uuid_str) - self.UNMASK_LEN

            # make the star mask
            stars = "*" * star_count
            # get the bit we want to leave unmasked
            _last_five = self.user_uuid[-(self.UNMASK_LEN):]

            # join the mask with the end part we're leaving unmasked
            uuid_str = stars + _last_five
        return uuid_str


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
