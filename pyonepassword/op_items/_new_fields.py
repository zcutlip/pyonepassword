from typing import Any

from ._new_field_registry import op_register_item_field_type
from .item_section import OPItemField, OPSection
from .uuid import OPUniqueIdentifierHex, is_uuid


class OPNewItemField(OPItemField):
    FIELD_TYPE = None

    def __init__(self, field_label: str, value: Any, field_id=None, section: OPSection = None):
        if not self.FIELD_TYPE:
            raise TypeError(
                f"{self.__class__.__name__} must be overridden and FIELD_TYPE set")

        if not field_id:
            unique_id = OPUniqueIdentifierHex()
            field_id = str(unique_id)
        field_dict = {
            "id": field_id,
            "label": field_label,
            "value": value,
            "type": self.FIELD_TYPE
        }
        if section:
            field_dict["section"] = dict(section)
        super().__init__(field_dict)
        if section:
            section.register_field(self)

    @classmethod
    def from_field(cls, field: OPItemField, section: OPSection = None):
        field_id = field["id"]
        if is_uuid(field_id):
            field_id = str(OPUniqueIdentifierHex())
        label = field["label"]
        value = field["label"]
        new_field = cls(label, value, field_id=field_id, section=section)
        return new_field


@op_register_item_field_type
class OPNewStringField(OPNewItemField):
    FIELD_TYPE = "STRING"


@op_register_item_field_type
class OPNewConcealedField(OPNewItemField):
    FIELD_TYPE = "CONCEALED"
