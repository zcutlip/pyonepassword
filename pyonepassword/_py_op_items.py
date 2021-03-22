from abc import ABC, abstractmethod
from typing import Dict, List


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
    def uuid(self) -> str:
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

class OPAbstractItem(ABC):
    TEMPLATE_ID = None

    @abstractmethod
    def __init__(self, item_dict):
        self._item_dict = item_dict

    def primary_section_field_value(self, field_label):
        first_sect = self.first_section
        field_value = self._field_value_from_section(first_sect, field_label)
        return field_value

    @property
    def uuid(self) -> str:
        return self._item_dict["uuid"]

    @property
    def title(self) -> str:
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

    @property
    def first_section(self) -> OPSection:
        first = None
        if self.sections:
            first = self.sections[0]
            first = OPSection(first)
        return first

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
        field_value = None
        details = self._item_dict["details"]
        field_value = details[field_designation]

        return field_value


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
class OPCreditCardItem(OPAbstractItem):
    TEMPLATE_ID = "002"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    def credit_card_details(self) -> OPSection:
        details = self.first_section
        return details

    def additional_details(self) -> OPSection:
        details = self.sections_by_title("Additional Details")[0]
        return details

    def primary_details_item(self, field_label: str):
        details = self.credit_card_details()
        item_value = self._details_item(details, field_label)
        return item_value

    def addl_details_item(self, field_label: str):
        details = self.additional_details()
        item_value = self._details_item(details, field_label)
        return item_value

    @property
    def credit_card_number(self):
        ccnum = self.primary_details_item("number")
        return ccnum

    @property
    def cvv(self):
        ccv = self.primary_details_item("verification number")
        return ccv

    @property
    def expiry_date(self) -> int:
        exp_date = self.primary_details_item("expiry date")
        return exp_date

    @property
    def valid_from(self) -> int:
        valid_from = self.primary_details_item("valid from")
        return valid_from

    @property
    def pin(self):
        pin = self.addl_details_item("PIN")
        return pin

    @property
    def credit_limit(self):
        climit = self.addl_details_item("credit limit")
        return climit

    @property
    def cash_withdrawal_limit(self):
        cw_limit = self.addl_details_item("cash withdrawal limit")
        return cw_limit

    @property
    def interest_rate(self):
        int_rate = self.addl_details_item("interest rate")
        return int_rate

    @property
    def issue_number(self):
        issue_num = self.addl_details_item("issue number")
        return issue_num

    def _details_item(self, details: OPSection, field_label: str):
        item_field: OPSectionField = details.fields_by_label(field_label)[0]
        item_value = item_field.value
        return item_value

@op_register_item_type
class OPSecureNoteItem(OPAbstractItem):
    TEMPLATE_ID = "003"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def note_text(self):
        text = self.get_item_field_value("notesPlain")
        return text

@op_register_item_type
class OPPasswordItem(OPAbstractItem):
    TEMPLATE_ID = "005"

    def __init__(self, item_dict):
        super().__init__(item_dict)

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
