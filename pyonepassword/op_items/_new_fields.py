import base64
import binascii
import urllib
from typing import Any, Optional, Union

from ._new_field_registry import op_register_new_item_field_type
from .item_field import OPItemField
from .item_section import OPSection
from .uuid import OPUniqueIdentifierBase32, is_uuid


class OPNewTOTPUriException(Exception):
    pass


class OPNewItemField(OPItemField):
    """
    A class for creating new fields for use with new items

    New fields may be created directly, or from existing fields
    """
    FIELD_TYPE = Optional[None]
    FIELD_PURPOSE = Optional[None]

    def __init__(self, field_label: str, value: Any, field_id=None, section: Optional[OPSection] = None):
        """
        Create a new field object

        NOTE: This class must be subclassed and FIELD_TYPE overridden

        Parameters
        ----------
        field_label: str
            The user-visible name of the field
        field_id: str, optional
            The unique identifier for this field. If none is provided, a random one will be generated
        section: OPSection, optional
            The section this field should be associated with. Not all fields are in sections
        """
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
    def from_field(cls, field: OPItemField, section: Optional[OPSection] = None):
        """
        Create a new field from an existing one

        If the existing field's ID is a random ID, a new random ID will be generated

        Parameters
        ----------
        field: OPItemField
            The field object to duplicate
        section: OPSection, optional
            The section this field should be associated with. Not all fields are in sections
        Returns
        -------
        new_field: OPItemField
            The newly created field object
        """
        field_id = field["id"]
        if is_uuid(field_id):
            field_id = str(OPUniqueIdentifierBase32())
        label = field["label"]
        value = field["value"]
        new_field = cls(label, value, field_id=field_id, section=section)
        return new_field


@op_register_new_item_field_type
class OPNewStringField(OPNewItemField):
    """
    A class for creating a new item field of type 'STRING'
    """
    FIELD_TYPE = "STRING"


@op_register_new_item_field_type
class OPNewConcealedField(OPNewItemField):
    """
    A class for creating a new item field of type 'CONCEALED'
    """
    FIELD_TYPE = "CONCEALED"


class OPNewUsernameField(OPNewStringField):
    """
    A class for creating a new specialized item field of type 'STRING' and purpose 'USERNAME'
    """
    FIELD_PURPOSE = "USERNAME"


class OPNewPasswordField(OPNewConcealedField):
    """
    A class for creating a new specialized item field of type 'CONCEALED' and purpose 'PASSWORD'
    """
    FIELD_PURPOSE = "PASSWORD"


class OPNewTOTPUri:
    """
    A class for constructing a properly formed TOTP URI from a secret, account name, and issuer
    """
    # otpauth://totp/<website>:<user>?secret=<secret>&issuer=<issuer>'
    # https://rootprojects.org/authenticator/

    def __init__(self,
                 secret: str,
                 account_name: Optional[str] = None,
                 issuer: Optional[str] = None):
        """
        Create a new OPNewTOTPUri object for use with a OPNewTOTPField

        Parameters
        ----------
        secret: str
            The base32-encoded secret seed for the TOTP generator.
            The base32 padding should be stripped. This value will be
            verified via base32 decoding
        account_name: str, optional
            The name of the account this TOTP is for. Defaults to "secret"
        issuer: str, optional
            The website or issuer for this TOTP object

        Raises
        ------
        OPNewTOTPUriException
            If the secret fails base32 decode verification
        """
        self._secret = secret
        self._issuer = issuer
        self._account = account_name or "secret"
        self._verify_secret()

    def _verify_secret(self):
        # Re-pad the secret and attempt to base32 decode it
        # raise an exception if decoding fails
        secret = self._secret
        missing_padding = len(secret) % 8
        if missing_padding != 0:
            secret += "=" * (8 - missing_padding)
        try:
            base64.b32decode(secret, casefold=True)
        except binascii.Error as e:
            raise OPNewTOTPUriException(
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


@op_register_new_item_field_type
class OPNewTOTPField(OPNewStringField):
    """
    A class for creating a new item field of type 'OTP'
    """
    FIELD_TYPE = "OTP"

    def __init__(self,
                 field_label: str,
                 totp_value: Union[str, OPNewTOTPUri],
                 field_id=None,
                 section: Optional[OPSection] = None):
        """
        Create a new TOTP field object


        Parameters
        ----------
        field_label: str
            The user-visible name of the field
        totp_value: Union[str, OPNewTOTPUri]
            The TOTP URI value for this field. May be a string or a OPNewTOTPUri object
        field_id: str, optional
            The unique identifier for this field. If none is provided, a random one will be generated
        section: OPSection, optional
            The section this field should be associated with. Not all fields are in sections
        """
        if isinstance(totp_value, OPNewTOTPUri):
            totp_value = str(totp_value)
        super().__init__(field_label, totp_value, field_id, section)
