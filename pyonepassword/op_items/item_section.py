import copy
import uuid
import binascii

from typing import Dict, List, Any, Union


class OPSectionFieldCollisionException(Exception):
    pass


class OPSectionCollisionException(Exception):
    pass


class OPSectionField(dict):
    def __init__(self, field_dict, deep_copy=True):
        # Let's make a copy so we don't modify the original
        if deep_copy:
            _dict = copy.deepcopy(field_dict)
        else:
            _dict = field_dict
        super().__init__(_dict)

    @classmethod
    def new_field(cls, name, value, field_type, label):
        field_dict = {
            "t": label,
            "v": value,
            "k": field_type,
            "n": name
        }
        obj = cls(field_dict)
        return obj

    @property
    def label(self) -> str:
        """
        Returns the field label as assigned and seen in the 1Password UI
        """
        return self["t"]

    @property
    def value(self) -> Any:
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
    def __init__(self, section_dict, deep_copy=True):
        if deep_copy:
            _dict = copy.deepcopy(section_dict)
        else:
            _dict = section_dict
        super().__init__(_dict)
        self._parse_fields()

    @classmethod
    def new_section(cls, name: str, title: str, fields: List[OPSectionField] = None):
        section_dict = {
            "name": name,
            "title": title
        }
        if fields is not None:
            section_dict["fields"] = fields
        obj = cls(section_dict)
        return obj

    @staticmethod
    def random_section_name():
        _uuid = uuid.uuid4()
        _uuid = binascii.hexlify(_uuid.bytes)
        uuid_str = _uuid.decode("utf-8")
        uuid_str = uuid_str.upper()
        section_name = f"Section_{uuid_str}"
        return section_name

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
        field_list = self.get("fields", [])
        return field_list

    @fields.setter
    def fields(self, fields: List[OPSectionField]):
        self["fields"] = fields

    def add_field(self, name: str, value: Union[str, int, Dict, List], field_type, label: str):
        # TODO: Validate field type against list of valid types

        for f in self.fields:
            if f.field_name == name:
                raise OPSectionFieldCollisionException(
                    f"Field with name {name} already exists in section {self.name}")
        new_field = OPSectionField.new_field(name, value, field_type, label)
        fields = self.fields
        fields.append(new_field)
        self.fields = fields
        return new_field

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

    def _parse_fields(self):
        _fields = self.get("fields")
        if _fields:
            field_list = []
            for field_dict in _fields:
                f = OPSectionField(field_dict, deep_copy=False)
                field_list.append(f)
            self["fields"] = field_list
