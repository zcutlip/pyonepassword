from typing import Optional

from .._item_descriptor_registry import op_register_item_descriptor_type
from .._item_type_registry import op_register_item_type
from ._item_base import OPAbstractItem, OPFieldNotFoundException
from ._item_descriptor_base import OPAbstractItemDescriptor


@op_register_item_descriptor_type
class OPServerItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "SERVER"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPServerItem(OPAbstractItem):
    CATEGORY = "SERVER"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def password(self) -> Optional[str]:
        password = self.field_value_by_id("password")
        return password

    @property
    def username(self) -> Optional[str]:
        username = self.field_value_by_id("username")
        return username

    @property
    def url(self) -> Optional[str]:
        try:
            url = self.field_value_by_id("url")
        except OPFieldNotFoundException:
            url = None
        return url

    @property
    def admin_console_password(self) -> Optional[str]:
        password = self.field_value_by_section_label(
            "Admin Console", "console password")
        return password

    @property
    def admin_console_username(self) -> Optional[str]:
        username = self.field_value_by_section_label(
            "Admin Console", "admin console username")
        return username

    @property
    def admin_console_url(self) -> Optional[str]:
        url = self.field_value_by_section_label(
            "Admin Console", "admin console URL")
        return url

    @property
    def hosting_provider_name(self) -> Optional[str]:
        """
        Convenience property to retrieve the hosting provider name

        Returns
        -------
        str
            name of the hosting provider
        """
        # Note: the actual field ID and label are "name"
        # so we look it up by section to be sure
        return self.field_value_by_section_label("Hosting Provider", "name")

    @property
    def hosting_provider_website(self) -> Optional[str]:
        """
        Convenience property to retrieve the hosting provider website

        Returns
        -------
        str
            Value of the hosting provider website field
        """
        # Note: the actual field ID and label are "name"
        # so we look it up by section to be sure
        return self.field_value_by_section_label("Hosting Provider", "website")

    @property
    def support_contact_url(self) -> Optional[str]:
        """
        Convenience property to retrieve the hosting provider support URL

        Returns
        -------
        str
            Value of the hosting provider support URL field
        """
        url = self.field_value_by_id("support_contact_url")
        return url

    @property
    def support_contact_phone(self) -> Optional[str]:
        """
        Convenience property to retrieve the hosting provider support phone

        Returns
        -------
        str
            Value of the hosting provider support phone field
        """
        phone = self.field_value_by_id("support_contact_phone")
        return phone


@op_register_item_type
class OPServerItemRelaxedValidation(OPServerItem):
    _relaxed_validation = True
