from .field_registry import op_register_item_field_type
from .item_field_base import OPItemField


@op_register_item_field_type
class OPStringField(OPItemField):
    FIELD_TYPE = "STRING"


@op_register_item_field_type
class OPConcealedField(OPItemField):
    FIELD_TYPE = "CONCEALED"


@op_register_item_field_type
class OPTOTPField(OPStringField):
    FIELD_TYPE = "OTP"

    @property
    def totp_secret(self) -> str:
        return self.value

    @property
    def totp(self) -> str:
        return self["totp"]
