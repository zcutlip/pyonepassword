from typing import Dict, List

class OPSectionField(dict):
    def __init__(self, field_dict):
        super().__init__(field_dict)

    @property
    def label(self) -> str:
        """
        Returns the field label as assigned and seen in the 1Password UI
        """
        return self["t"]

    @property
    def value(self) -> str:
        """
        Returns the field's value (password, URL, etc.) as assigned and seen in the 1Password UI,
        or None if the field lacks a value
        """
        v = self.get("v")
        return v

    @property
    def field_type(self) -> str:
        """
        Returns the field's type, which affects how the field's value is rendered in 1Password
        """
        return self["k"]

    @property
    def field_name(self) -> str:
        """
        Returns the field's unique identifier, which is not visible in the 1Password UI
        """
        return self["n"]

    @property
    def attributes(self) -> Dict[str, str]:
        attr_dict = self.get("a")
        return attr_dict


class OPSection(dict):
    def __init__(self, section_dict):
        super().__init__(section_dict)

    @property
    def name(self) -> str:
        """
        Returns the actual section name which may or may not be related to
        the user-visible title.
        It may be a lower-case transformation, like 'additional passwords'
        Or it may be something completely opaque, like
        'Section_967FEBAC931841BCBD2DD7CFE0B8DC82'
        """
        return self["name"]

    @property
    def title(self) -> str:
        """
        Returns the 'name' of the section as seen in the 1Password UI
        """
        return self["title"]

    @property
    def fields(self) -> List[OPSectionField]:
        _fields = self.get("fields")
        field_list = []

        if _fields:
            for field_dict in _fields:
                f = OPSectionField(field_dict)
                field_list.append(f)
        return field_list

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
