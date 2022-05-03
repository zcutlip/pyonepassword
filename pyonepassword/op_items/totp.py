from ..json import safe_unjson


class OPTOTPItem(dict):
    """
    {
        "id": "TOTP_obe3whgcenxulnxs5cjyjy763i",
        "section": {
            "id": "add more"
        },
        "type": "OTP",
        "label": "one-time password",
        "value": "AAAAY3DPEHPK3PXP",
        "totp": "368006",
        "reference": "op://Test Data/Login With TOTP/add more/one-time password"
    }
    """

    def __init__(self, totp_dict_or_json):
        totp_dict = safe_unjson(totp_dict_or_json)
        super().__init__(totp_dict)

    @property
    def unique_id(self) -> str:
        return self["id"]

    @property
    def totp(self) -> str:
        return self["totp"]

    @property
    def value(self) -> str:
        return self["value"]

    @property
    def label(self) -> str:
        return self["label"]

    @property
    def reference(self) -> str:
        return self["reference"]
