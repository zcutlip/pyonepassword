from .expected_item import ExpectedItemBase, ExpectedItemData


class ExpectedTOTP(ExpectedItemBase):
    """
    "Login With TOTP":{
            "id": "TOTP_obe3whgcenxulnxs5cjyjy763i",
            "section": {
                "id": "add more"
            },
            "type": "OTP",
            "label": "one-time password",
            "value": "AAAAY3DPEHPK3PXP",
            "totp": "741354",
            "reference": "op://Test Data/Login With TOTP/add more/one-time password"
        }
    """

    @property
    def unique_id(self) -> str:
        return self._data["id"]

    @property
    def label(self) -> str:
        return self._data["label"]

    @property
    def value(self) -> str:
        return self._data["value"]

    @property
    def totp(self) -> str:
        return self._data["totp"]

    @property
    def reference(self) -> str:
        return self._data["reference"]


class ExpectedTOTPData(ExpectedItemData):

    def totp_data_for_login(self, login_identifier):
        item_dict = self.data_for_name(login_identifier)
        login_item = ExpectedTOTP(item_dict)
        return login_item
