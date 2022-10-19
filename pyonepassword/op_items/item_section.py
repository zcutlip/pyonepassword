import copy
from typing import List

from .item_field_base import OPItemField


class OPItemFieldCollisionException(Exception):
    pass


class OPSectionCollisionException(Exception):
    pass


class OPSection(dict):
    def __init__(self, section_dict):
        super().__init__(section_dict)
        # shadow fields map makes it easy to detect collisions
        # by looking up a field's ID to see if it's already been registered
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
            # make a copy of the field so we don't end up with a circular reference
            field = copy.copy(field_dict)
        else:
            field = OPItemField(field_dict)
        field_id = field.field_id
        if field_id in self._shadow_fields:
            raise OPItemFieldCollisionException(
                f"Field {field_id} already registered in section {self.section_id}")
        self.fields.append(field)
        self._shadow_fields[field_id] = field

    def fields_by_label(self, label, case_sensitive=True) -> List[OPItemField]:
        """
        Returns all fields in a section matching the given label.
        Fields are not required to have unique labels, so there may be more than one match.
        """
        matching_fields = []
        f: OPItemField
        for f in self.fields:
            f_label = f.label
            if not case_sensitive:
                f_label = f_label.lower()
                label = label.lower()
            if f_label == label:
                matching_fields.append(f)
        return matching_fields

    def first_field_by_label(self, label: str, case_sensitive=True):
        """
        Convenience function for when you're certain there's only one field
        by a given label, or don't really care for whatever reason
        """
        fields = self.fields_by_label(label, case_sensitive=case_sensitive)
        f = fields[0]
        return f
