from typing import List, Optional, Union

from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._new_fields import OPNewPasswordField, OPNewUsernameField
from ._new_item import OPNewItemMixin
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem
from .item_field_base import OPItemField
from .item_section import OPSection


class OPNewLoginItemURLException(Exception):
    pass


@op_register_item_descriptor_type
class OPLoginDescriptorItem(OPAbstractItemDescriptor):
    CATEGORY = "LOGIN"

    def __init__(self, item_dict):
        super().__init__(item_dict)


class OPLoginItemURL(dict):
    def __init__(self, url_dict):
        super().__init__(url_dict)

    @property
    def label(self) -> Optional[str]:
        return self.get("label")

    @property
    def primary(self) -> Optional[bool]:
        primary = self.get("primary", False)
        return primary

    @property
    def href(self) -> str:
        return self["href"]


class OPLoginItemNewURL(OPLoginItemURL):
    """
    A class to create a new URL dictionary for use with OPLoginItemTemplate
    """

    def __init__(self, url: str, label: str, primary: bool = False):
        """
        Create a new OPLoginItemNewURL object

        Parameters
        ----------
        url: str
            The URL for this object
        label: str
            The user-visible name of the URL entry
        primary: bool, optional
            Whether this URL should be flagged as primary. Defaults to False
            NOTE: There can only be one primary URL in a login item
        """
        url_dict = {
            "label": label,
            "primary": primary,
            "href": url
        }
        super().__init__(url_dict)


class OPLoginItemNewPrimaryURL(OPLoginItemNewURL):
    """
    A class to create a new primary URL dictionary for use with OPLoginItemTemplate
    """

    def __init__(self, url: str, label: str):
        super().__init__(url, label, primary=True)


@op_register_item_type
class OPLoginItem(OPAbstractItem):
    CATEGORY = "LOGIN"

    def __init__(self, item_dict_or_json):
        super().__init__(item_dict_or_json)
        urls = []
        primary_url = None
        url_list = self.get("urls", [])
        for url_dict in url_list:
            url = OPLoginItemURL(url_dict)
            if url.primary:
                primary_url = url
            urls.append(url)
        self._urls = urls
        self._primary_url = primary_url

    @property
    def username(self):
        username = self.field_value_by_id("username")
        return username

    @property
    def password(self):
        password = self.field_value_by_id("password")
        return password

    @property
    def urls(self) -> List[OPLoginItemURL]:
        return self._urls

    @property
    def primary_url(self) -> OPLoginItemURL:
        return self._primary_url


class OPLoginItemTemplate(OPNewItemMixin, OPLoginItem):
    """
    Class for creating a login item template that can be used to create a new login item in 1Password
    """

    PASSWORDS_SUPPORTED = True

    FIELD_ID_USERNAME = "username"
    FIELD_ID_PASSWORD = "password"
    DEFAULT_URL_LABEL = "website"

    def __init__(self,
                 title: str,
                 username: str,
                 password: Optional[str] = None,
                 url: Union[str, OPLoginItemURL, None] = None,
                 fields: List[OPItemField] = [],
                 sections: List[OPSection] = []):
        """
        Create an OPLoginItemTemplate object that can be used to create a new login item entry

        Parameters
        ----------
        Title : str
            User viewable name of the login item to create
        username : str
            username string for the new login item
        password : str, optional
            password to set for this login item
        url: Union[str, OPLoginItemURL] = None
            If provided, set to the primary URL of the login item
            If URL is a str, it is converted to OPLoginItemURL, with label="website"
        fields: List[OPItemField]
            List of OPItemField objects to associate with the item.
            NOTE: If the fields are from an exisiting item, and the field IDs are UUIDs, the field IDs will be regenerated
        sections: List[OPSection]
            List of OPSection objects to associate with the item.
            NOTE: If the sections are from an exisiting item, and the section IDs are UUIDs, the section IDs will be regenerated

        Raises
        ------
        OPNewLoginItemURLException
            If an OPUrlItem object is provided to the constructor, and it's not flagged as a primary URL
        """
        if sections is None:  # pragma: no coverage
            sections = []
        else:
            sections = list(sections)
        if fields is None:  # pragma: no coverage
            fields = []
        else:
            fields = list(fields)

        if isinstance(url, str):
            url = OPLoginItemNewPrimaryURL(url, self.DEFAULT_URL_LABEL)

        username_field = OPNewUsernameField(
            self.FIELD_ID_USERNAME,
            username,
            field_id=self.FIELD_ID_USERNAME
        )

        password_field = OPNewPasswordField(
            self.FIELD_ID_PASSWORD,
            password,
            field_id=self.FIELD_ID_PASSWORD
        )

        fields.extend([username_field, password_field])
        urls = []
        if url:
            if not url.primary:
                raise OPNewLoginItemURLException("Sole URL must be primary")
            urls.append(url)
        extra_data = {"urls": urls}
        super().__init__(title, sections=sections, fields=fields, extra_data=extra_data)

    def add_url(self, url: OPLoginItemURL):
        """
        Add a URL to this login item

        Parameters
        ----------
        url: OPLoginItemURL
            The URL to add to this login item

        Raises
        ------
        OPNewLoginItemURLException
            If the URL object is a primary URL, and there is already a primary URL
        """
        has_primary = False
        if self.primary_url:
            has_primary = True
        if url.primary and has_primary:
            raise OPNewLoginItemURLException("Can't add multiple primary URLs")

        self._urls.append(url)
        if url.primary:
            self._primary_url = url
