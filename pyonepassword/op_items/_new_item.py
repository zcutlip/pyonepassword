import json
import os
import tempfile
from typing import Dict, List, Optional

from ..py_op_exceptions import OPInvalidItemException
from ._new_field_registry import OPNewItemField, OPNewItemFieldFactory
from .item_field_base import OPItemField
from .item_section import OPSection, OPSectionCollisionException
from .template_directory import OPTemplateDirectory
from .uuid import OPUniqueIdentifierBase32, is_uuid


class OPNewItemDataCollisionException(Exception):
    pass


class OPNewSection(OPSection):
    """
    A class for creating new sections for use with new items

    New sections may be created directly, or from existing sections
    """

    def __init__(self, section_label: str, section_id: Optional[str] = None):
        """
        Create a new section object

        Parameters
        ----------
        section_label: str
            The user-visible name of the section
        section_id: str, optional
            The unique identifier for this section. If none is provided, a random one will be generated
        """
        if not section_id:
            unique_id = OPUniqueIdentifierBase32()
            section_id = str(unique_id)
        section_dict = {
            "id": section_id,
            "label": section_label
        }
        super().__init__(section_dict)

    @classmethod
    def from_section(cls, section: OPSection):
        """
        Create a new section from an existing one

        If the existing section's ID is a random ID, a new random ID will be generated

        Parameters
        ----------
        section: OPSection
            The section object to duplicate

        Returns:
        new_section: OPNewSection
            The newly created section object
        """
        section_id = section.section_id
        if is_uuid(section_id):
            section_id = str(OPUniqueIdentifierBase32())
        label = section.label
        return cls(label, section_id=section_id)


class OPNewItemMixin:
    """
    A class that, when subclassed along with one of the item classes (OPLogin, etc.), allows a
    item of that type to be created from a template
    E.g.,
    class OPLoginItemTemplate(OPNewItemMixin, OPLoginItem):
        ...

    NOTE: It is essential OPNewItemMixin be named first, so its `__init_()` gets called first
    """

    # Whether this item type can have a password generated
    # override for item types that do support passwords (e.g., Login)
    PASSWORDS_SUPPORTED = False

    def __init__(self, title: str, fields: List[OPItemField] = [], sections: List[OPSection] = [], extra_data={}):
        """
        Create an OPNewItemMixin object that can be used to create a new item entry

        Parameters
        ----------
        Title : str
            User viewable name of the item to create
        fields: List[OPItemField], optional
            List of OPItemField objects to associate with the item.
            NOTE: If the fields are from an exisiting item, and the field IDs are UUIDs, the field IDs will be regenerated
        sections: List[OPSection], optional
            List of OPSection objects to associate with the item.
            NOTE: If the sections are from an exisiting item, and the section IDs are UUIDs, the section IDs will be regenerated

        extra_data: Dict[str, Any]
            Dictionary of data not associated with any field or section, for example login item URLs:
            {
                "urls": [
                    {
                        "label": "example website 2",
                        "href": "http://example2.website"
                    },
                    {
                        "label": "example website 1",
                        "primary": true,
                        "href": "https://example.website"
                    }
                ]
            }

        Raises
        ------
        OPSectionCollisionException
            If two or more sections have conflicting section IDs
        OPNewItemDataCollisionException
            If one or more keys in extra_data is already present in this item
        OPInvalidItemException
            If the subclass does not also inherit from a valid OPAbstractItem implementation
        """
        if sections is None:  # pragma: no coverage
            sections = []
        else:
            sections = list(sections)
        if fields is None:  # pragma: no coverage
            fields = []
        else:
            fields = list(fields)
        if extra_data is None:  # pragma: no coverage
            extra_data = {}
        else:
            extra_data = dict(extra_data)

        directory = OPTemplateDirectory()

        # Mostly this satisfies mypy since OPNewItemMixin intentionally
        # doesn't define a CATEGORY attribute
        # my preference would be to not handle it and allow attribute error to blow
        # things up, but since we do have to check first, lets just raise
        # a descriptive OPInvalidItemException
        if hasattr(self, "CATEGORY"):
            template_dict: Dict = directory.template_for_category(
                self.CATEGORY)
        else:
            raise OPInvalidItemException(
                "Item template class inherit also from inherit a concreate OPAbstractItem implementation, overriding CATEGORY")
        template_dict["title"] = title
        section_map = {}
        new_sections = []
        new_fields = []
        old_to_new_sections = {}

        for sect in sections:
            if not isinstance(sect, OPNewSection):
                old_id = sect.section_id
                sect = OPNewSection.from_section(sect)
                # create a mapping of old-to-new sections to keep
                # up with the sections whose UUIDs get regenerated
                old_to_new_sections[old_id] = sect
            if sect.section_id in section_map:
                raise OPSectionCollisionException(
                    f"Duplicate section ID when creating new sections: {sect.section_id}")
            section_map[sect.section_id] = sect
            new_sections.append(sect)

        for field in fields:
            section_id = field.section_id
            if not isinstance(field, OPNewItemField):
                section = None
                if section_id:
                    section = old_to_new_sections.get(section_id)
                field = OPNewItemFieldFactory.item_field(
                    field, section=section)
            else:

                section = old_to_new_sections.get(
                    section_id) if section_id else None
                if section:
                    # If a section's UUID may have been regenerated, we need to re-link it to the field
                    field.update_section(sect)
            new_fields.append(field)
        template_dict["sections"] = new_sections
        template_dict["fields"] = new_fields
        key_collisions = []

        for key in extra_data.keys():
            if key in self:  # type: ignore
                #                    mypy doesn't like this even though it's fine later
                #                    and if it isn't we should ust blow up anyway
                key_collisions.append(key)  # pragma: no coverage
        if key_collisions:
            raise OPNewItemDataCollisionException(  # pragma: no coverage
                f"Extra data key collisions: {key_collisions}")
        if extra_data:
            template_dict.update(extra_data)

        # Satisfy mypy: Too many arguments for "__init__" of "object"
        args = [template_dict]
        super().__init__(*args)
        self._temp_files: List[str] = []

    def secure_tempfile(self, encoding="utf8") -> str:
        """
        Serialize this item object to a secure temp file for use during 'op item create'

        The temporary file is deleted when this object goes out of scope

        Parameters
        ----------
        encoding: str, optional
            Encoding to use when serializing to file. Defaults to "utf-8"

        Returns
        -------
        temp.name: str
            The name of the temporary file
        """
        temp = tempfile.NamedTemporaryFile(
            mode="w", delete=False, encoding=encoding)
        self._temp_files.append(temp.name)
        json.dump(self, temp)
        temp.close()
        return temp.name

    def supports_passwords(self) -> bool:
        """
        Whether passwords are applicable items of this type

        Returns
        -------
        password_supported: bool
        """
        return self.PASSWORDS_SUPPORTED

    def __del__(self):

        # if we blow up during object initialization
        # _temp_files may not exist, so check first
        if hasattr(self, "_temp_files"):
            while self._temp_files:
                t = self._temp_files.pop()
                try:
                    os.unlink(t)
                except FileNotFoundError:
                    continue
