import base64
import binascii
import urllib
from typing import Any, Optional, Union

from ._new_field_registry import op_register_item_field_type
from .item_section import OPItemField, OPSection
from .uuid import OPUniqueIdentifierBase32, is_uuid


class OPNewTOTPUrlException(Exception):
    pass


class OPNewItemField(OPItemField):
    FIELD_TYPE = None
    FIELD_PURPOSE = None

    def __init__(self, field_label: str, value: Any, field_id=None, section: OPSection = None):
        if not self.FIELD_TYPE:  # pragma: no cover
            raise TypeError(
                f"{self.__class__.__name__} must be overridden and FIELD_TYPE set")

        if not field_id:
            unique_id = OPUniqueIdentifierBase32()
            field_id = str(unique_id)
        field_dict = {
            "id": field_id,
            "label": field_label,
            "value": value,
            "type": self.FIELD_TYPE
        }
        if self.FIELD_PURPOSE:
            field_dict["purpose"] = self.FIELD_PURPOSE
        if section:
            field_dict["section"] = dict(section)
        super().__init__(field_dict)
        if section:
            section.register_field(self)

    def update_section(self, section: OPSection):
        """
        Update a field's associated section in the event
        a section's UUID was regenerated
        """
        if self.section_id != section.section_id:
            self["section"] = dict(section)
            section.register_field(self)

    @classmethod
    def from_field(cls, field: OPItemField, section: OPSection = None):
        field_id = field["id"]
        if is_uuid(field_id):
            field_id = str(OPUniqueIdentifierBase32())
        label = field["label"]
        value = field["value"]
        new_field = cls(label, value, field_id=field_id, section=section)
        return new_field


@op_register_item_field_type
class OPNewStringField(OPNewItemField):
    FIELD_TYPE = "STRING"


@op_register_item_field_type
class OPNewConcealedField(OPNewItemField):
    FIELD_TYPE = "CONCEALED"


class OPNewUsernameField(OPNewStringField):
    FIELD_PURPOSE = "USERNAME"


class OPNewPasswordField(OPNewConcealedField):
    FIELD_PURPOSE = "PASSWORD"


class OPNewTOTPUrl:
    # otpauth://totp/<website>:<user>?secret=<secret>&issuer=<issuer>'
    # https://rootprojects.org/authenticator/
    def __init__(self,
                 secret: str,
                 account_name: Optional[str] = None,
                 issuer: Optional[str] = None):
        self._secret = secret
        self._issuer = issuer
        self._account = account_name or "secret"
        self._verify_secret()

    def _verify_secret(self):
        secret = self._secret
        missing_padding = len(secret) % 8
        if missing_padding != 0:
            secret += "=" * (8 - missing_padding)
        try:
            base64.b32decode(secret, casefold=True)
        except binascii.Error as e:
            raise OPNewTOTPUrlException(
                f"Invalid secret string: base32 decoding {e}")

    def __str__(self):
        issuer = None
        if self._issuer:
            issuer = urllib.parse.quote(self._issuer)
        account = urllib.parse.quote(self._account)
        if issuer:
            label = f"{issuer}:{account}"
        else:
            label = account

        params = {"secret": self._secret}

        if self._issuer:
            params["issuer"] = self._issuer

        params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        url_str = f"otpauth://totp/{label}?{params}"
        return url_str


@op_register_item_field_type
class OPNewTOTPField(OPNewStringField):
    FIELD_TYPE = "OTP"

    def __init__(self,
                 field_label: str,
                 totp_value: Union[str, OPNewTOTPUrl],
                 field_id=None,
                 section: OPSection = None):
        if isinstance(totp_value, OPNewTOTPUrl):
            totp_value = str(totp_value)
        super().__init__(field_label, totp_value, field_id, section)
