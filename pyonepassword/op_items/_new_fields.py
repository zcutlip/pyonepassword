from typing import Any

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
