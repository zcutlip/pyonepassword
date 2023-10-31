import base64
import binascii
import urllib.parse
from typing import Optional, Union

from .._new_field_registry import (
    OPNewItemField,
    op_register_new_item_field_type
)
from .item_section import OPSection


class OPNewTOTPUriException(Exception):
    pass


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

        params_dict = {"secret": self._secret}

        if self._issuer:
            params_dict["issuer"] = self._issuer

        params = urllib.parse.urlencode(
            params_dict, quote_via=urllib.parse.quote)
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
                 field_id: str = None,
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


class OPNewNetworkPortField(OPNewStringField):
    """
    A class for creating a new item string field for use with numeric port values.
    """

    def __init__(self, field_label: str, value: Union[str, int], field_id: str = None, section: Optional[OPSection] = None):
        """
        Create an OPNewNetworkPortField for use with new item template objects

        Parameters
        ----------
        field_label : str
            The user-visible name of the field
        value : Union[str, int]
            port value for the new database item, by default None
            Discussion:
                The port value may be either an integer or a string representation of an integer.

                If an integer is provided, it will be converted to a string via 'str(value)'

                If a string is provided, it will be validated by converting it to an integer via 'int(value, 0)'.
                If this fails, ValueError is raised.
                The string may be any valid base representation. E.g., 1234 or 0x1234. This representation will
                preserved.

                No attempt is made to ensure the value is in a reasonable range for what a port should be
        field_id : str, optional
            The unique identifier for this field. If none is provided, a random one will be generated. By default None
        section : OPSection, optional
            The section this field should be associated with. Not all fields are in sections, by default None

        Raises
        ------
        ValueError
            _description_
        """
        if isinstance(value, str):
            # convert to int for sanity checking
            # accept any base. int() will raise ValueError if it can't
            # be converted
            _ = int(value, 0)
        elif isinstance(value, int):
            # only convert 'value' to a string
            # if it wasn't already, in order to preserve alternate base representations
            # e.g., 0x4d2
            value = str(value)
        else:
            # if we were passed any other object type this is an error
            raise TypeError(
                f"Invalid value for port: \"{value}\". Must be int or str")

        # NOTE: we're not going to enforce valid, non-negative port ranges
        # user can enter whatever number they like

        super().__init__(field_label, value, field_id, section)
