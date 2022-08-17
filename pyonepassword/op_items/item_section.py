import copy
from typing import Any, List, Union


class OPItemFieldCollisionException(Exception):
    pass


class OPSectionCollisionException(Exception):
    pass


class OPItemField(dict):
    FIELD_TYPE = None

    def __init__(self, field_dict):
        super().__init__(field_dict)

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

    @property
    def reference(self) -> Union[str, None]:
        return self.get("reference")

    @property
    def purpose(self) -> str:
        return self["purpose"]

    @property
    def entropy(self) -> Union[float, None]:
        return self.get("entropy")

    @property
    def section_id(self) -> Union[str, None]:
        section_id = None
        section = self.get("section")
        if section:
            section_id = section["id"]
        return section_id


class OPSection(dict):
    def __init__(self, section_dict):
        super().__init__(section_dict)
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
    def fields(self) -> List[OPItemField]:
        field_list = self.setdefault("fields", [])
        return field_list

    def register_field(self, field_dict):
        if isinstance(field_dict, OPItemField):
            field = copy.copy(field_dict)
        else:
            field = OPItemField(field_dict)
        field_id = field.field_id
        if field_id in self._shadow_fields:
            raise OPItemFieldCollisionException(
                f"Field {field_id} already registered in section {self.section_id}")
        self.fields.append(field)
        self._shadow_fields[field_id] = field

    def fields_by_label(self, label) -> List[OPItemField]:
        """
        Returns all fields in a section matching the given label.
        Fields are not required to have unique labels, so there may be more than one match.
        """
        matching_fields = []
        f: OPItemField
        for f in self.fields:
            if f.label == label:
                matching_fields.append(f)
        return matching_fields

    def first_field_by_label(self, label: str):
        fields = self.fields_by_label(label)
        f = fields[0]
        return f
