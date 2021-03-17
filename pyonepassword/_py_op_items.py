from abc import ABC, abstractmethod
from typing import List


class OPUnknownItemType(Exception):
    def __init__(self, msg, item_dict=None):
        super().__init__(msg)
        self.item_dict = item_dict


class OPItemFactory:
    _TYPE_REGISTRY = {}

    @classmethod
    def register_op_item_type(cls, item_type, item_class):
        cls._TYPE_REGISTRY[item_type] = item_class

    @classmethod
    def op_item_from_item_dict(cls, item_dict):
        item_type = item_dict["templateUuid"]
        try:
            item_cls = cls._TYPE_REGISTRY[item_type]
        except KeyError as ke:
            raise OPUnknownItemType(
                "Unknown item type", item_dict=item_dict) from ke

        return item_cls(item_dict)


def op_register_item_type(item_class):
    item_type = item_class.TEMPLATE_ID
    OPItemFactory.register_op_item_type(item_type, item_class)

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
        Returns the field's value (password, URL, etc.) as assigned and seen in the 1Password UI
        """
        return self["v"]

    @property
    def field_type(self) -> str:
        """
        Returns the field's type, which affects how the field's value is rendered in 1Password
        """
        return self["k"]

    @property
    def uuid(self) -> str:
        """
        Returns the field's unique identifier, which is not visible in the 1Password UI
        """
        return self["n"]

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

class OPAbstractItem(ABC):
    TEMPLATE_ID = None

    @abstractmethod
    def __init__(self, item_dict):
        self._item_dict = item_dict

    @property
    def uuid(self):
        return self._item_dict["uuid"]

    @property
    def title(self):
        overview = self._item_dict["overview"]
        title = overview["title"]
        return title

    @property
    def sections(self) -> List[OPSection]:
        section_list = []
        _sections = self._item_dict['details'].get("sections")
        if _sections:
            for section_dict in _sections:
                s = OPSection(section_dict)
                section_list.append(s)
        return section_list

    def sections_by_title(self, title) -> List[OPSection]:
        """
        Returns a list of zero or more sections matching the given title.
        Sections are not required to have unique titles, so there may be more than one match.
        """
        matching_sections = []
        sect: OPSection
        for sect in self.sections:
            if sect.title == title:
                matching_sections.append(sect)

        return sect

    def get_item_field_value(self, field_designation):
        return None


@op_register_item_type
class OPLoginItem(OPAbstractItem):
    TEMPLATE_ID = "001"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    def get_item_field_value(self, field_designation):
        field_value = None
        details = self._item_dict["details"]
        fields = details["fields"]
        for f in fields:
            if f["designation"] == field_designation:
                field_value = f["value"]
                break
        return field_value

    @property
    def username(self):
        username = None
        details = self._item_dict["details"]
        fields = details["fields"]
        for f in fields:
            if f["designation"] == "username":
                username = f["value"]
                break

        return username

    @property
    def password(self):
        password = self.get_item_field_value("password")
        return password


@op_register_item_type
class OPPasswordItem(OPAbstractItem):
    TEMPLATE_ID = "005"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    def get_item_field_value(self, field_designation):
        field_value = None
        details = self._item_dict["details"]
        field_value = details[field_designation]

        return field_value

    @property
    def password(self):
        password = self.get_item_field_value("password")
        return password


@op_register_item_type
class OPDocumentItem(OPAbstractItem):
    TEMPLATE_ID = "006"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def file_name(self):
        details = self._item_dict["details"]
        document_attributes = details["documentAttributes"]
        file_name = document_attributes["fileName"]
        return file_name
