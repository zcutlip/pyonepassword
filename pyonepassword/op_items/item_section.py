import copy
import uuid
from typing import Any, List


def random_id():
    unique_id = uuid.uuid4()
    unique_id = unique_id.hex
    return unique_id


class OPSectionFieldCollisionException(Exception):
    pass


class OPSectionCollisionException(Exception):
    pass


class OPSectionField(dict):
    FIELD_TYPE = None

    def __init__(self, field_dict, deep_copy=True):
        # Let's make a copy so we don't modify the original
        if deep_copy:
            _dict = copy.deepcopy(field_dict)
        else:
            _dict = field_dict
        super().__init__(_dict)

    @classmethod
    def new_field(cls, value, field_label, field_id=None):
        if not field_id:
            field_id = random_id()

        if cls.FIELD_TYPE is None:
            raise NotImplementedError("Use subclass that overrides FIELD_TYPE")
        field_dict = {
            "id": field_id,
            "type": cls.FIELD_TYPE,
            "label": field_label,
            "value": value,
        }
        obj = cls(field_dict)
        return obj

    @property
    def field_id(self) -> str:
        return self["id"]

    @property
    def label(self) -> str:
        """
        Returns the field label as assigned and seen in the 1Password UI
        """
        return self["label"]

    @property
    def value(self) -> Any:
        """
        Returns the field's value (password, URL, etc.) as assigned and seen in the 1Password UI,
        or None if the field lacks a value
        """
        v = self.get("value")
        return v

    @property
    def field_type(self) -> str:
        """
        Returns the field's type, which affects how the field's value is rendered in 1Password
        """
        return self["type"]


class OPStringField(OPSectionField):
    FIELD_TYPE = "string"


class OPConcealedField(OPSectionField):
    FIELD_TYPE = "concealed"


class OPSection(dict):
    def __init__(self, section_dict, deep_copy=True):
        if deep_copy:
            _dict = copy.deepcopy(section_dict)
        else:
            _dict = section_dict
        super().__init__(_dict)
        self._shadow_fields = {}

    @property
    def section_id(self) -> str:
        """
        Returns the section ID which may or may not be related to
        the user-visible title.
        It may be a lower-case transformation, like 'additional passwords'
        Or it may be something completely opaque, like
        'Section_967FEBAC931841BCBD2DD7CFE0B8DC82'
        """
        return self["id"]

    @property
    def label(self) -> str:
        """
        Returns the 'name' of the section as seen in the 1Password UI
        """
        return self["label"]

    @property
    def fields(self) -> List[OPSectionField]:
        field_list = self.setdefault("fields", [])
        return field_list

    def register_field(self, field_dict):
        field = OPSectionField(field_dict)
        field_id = field.field_id
        if field_id in self._shadow_fields:
            raise OPSectionFieldCollisionException(
                f"Field {field_id} already registered in section {self.section_id}")
        self.fields.append(field)
        self._shadow_fields[field_id] = field

    def fields_by_label(self, label) -> List[OPSectionField]:
        """
        Returns all fields in a section matching the given label.
        Fields are not required to have unique labels, so there may be more than one match.
        """
        matching_fields = []
        f: OPSectionField
        for f in self.fields:
            if f.label == label:
                matching_fields.append(f)
        return matching_fields
