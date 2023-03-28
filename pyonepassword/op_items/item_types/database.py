from typing import List, Union

from .._item_descriptor_registry import op_register_item_descriptor_type
from .._item_type_registry import op_register_item_type
from .._new_item import OPNewItemMixin
from ..fields_sections._new_fields import (
    OPNewConcealedField,
    OPNewNetworkPortField,
    OPNewStringField
)
from ..fields_sections.item_field import OPItemField
from ..fields_sections.item_section import OPSection
from ._item_base import OPAbstractItem, OPFieldNotFoundException
from ._item_descriptor_base import OPAbstractItemDescriptor


@op_register_item_descriptor_type
class OPDatabaseItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "DATABASE"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPDatabaseItem(OPAbstractItem):
    CATEGORY = "DATABASE"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def database_type(self) -> str:
        try:
            database_type = self.field_value_by_id("database_type")
        except OPFieldNotFoundException:  # pragma: no coverage
            database_type = None
        return database_type

    @property
    def type(self) -> str:
        # convenience accessor for "database_type"
        # label for "database_type" is "type"
        return self.database_type

    @property
    def hostname(self) -> str:
        try:
            hostname = self.field_value_by_id("hostname")
        except OPFieldNotFoundException:
            hostname = None
        return hostname

    @property
    def server(self) -> str:
        # convenience accessor for "hostname"
        # label for "hostname" is "server"
        return self.hostname

    @property
    def port(self) -> int:
        try:
            port = self.field_value_by_id("port")
        except OPFieldNotFoundException:
            port = None
        return port

    @property
    def database(self) -> Union[str, None]:
        try:
            database = self.field_value_by_id("database")
        except OPFieldNotFoundException:
            database = None
        return database

    @property
    def username(self) -> str:
        try:
            username = self.field_value_by_id("username")
        except OPFieldNotFoundException:
            username = None
        return username

    @property
    def password(self) -> str:
        try:
            password = self.field_value_by_id("password")
        except OPFieldNotFoundException:
            password = None
        return password

    @property
    def sid(self) -> Union[str, None]:
        try:
            sid = self.field_value_by_id("SID")
        except OPFieldNotFoundException:
            sid = None
        return sid

    @property
    def alias(self) -> Union[str, None]:
        try:
            alias = self.field_value_by_id("alias")
        except OPFieldNotFoundException:
            alias = None
        return alias

    @property
    def options(self) -> Union[str, None]:
        try:
            options = self.field_value_by_id("options")
        except OPFieldNotFoundException:
            options = None
        return options

    @property
    def connection_options(self) -> Union[str, None]:
        # convenience accessor for "options"
        # label for "options" field is "connection options"
        return self.options


@op_register_item_type
class OPDatabaseItemRelaxedValidation(OPDatabaseItem):
    # see ITEM_VALIDATION.md
    _relaxed_validation = True


class OPDatabaseItemTemplate(OPNewItemMixin, OPDatabaseItem):
    """
    Class for creating a database item template that can be used to create a new database item in 1Password
    """

    # Not setting PASSWORDS_SUPPORTED = True
    # because 'op' only supports password creation for LOGIN and PASSWORD
    # item types

    def __init__(self,
                 title: str,
                 database_type: str = None,
                 hostname: str = None,
                 port: Union[str, int] = None,
                 database: str = None,
                 username: str = None,
                 password: str = None,
                 sid: str = None,
                 alias: str = None,
                 options: str = None,
                 fields: List[OPItemField] = [],
                 sections: List[OPSection] = [],
                 tags: List[str] = []):
        """
        Create an OPDatabaseItemTemplate object that can be used to create a new database item entry

        Parameters
        ----------
        title : str
            User viewable name of the database item to create
        database_type : str, optional
            Value for the database type field, by default None
        hostname : str, optional
            Value for the hostname/server field, by default None
        port : Union[str, int], optional
            port value for the new database item, by default None
            Discussion:
                The port value may be either an integer or a string representation of an integer.

                If an integer is provided, it will be converted to a string via 'str(value)'

                If a string is provided, it will be validated by converting it to an integer via 'int(value, 0)'.
                If this fails, ValueError is raised.
                The string may be any valid base representation. E.g., 1234 or 0x1234. This representation will
                preserved.

                No attempt is made to ensure the value is in a reasonable range for what a port should be

        database : str, optional
            Value for the database field, by default None
        username : str, optional
            Value for the username field, by default None
        password : str, optional
            Value for the password field, by default None
        sid : str, optional
            Value for the SID field, by default None
        alias : str, optional
            Value for the alias field, by default None
        options : str, optional
            Value for the connection options field, by default None
        fields: List[OPItemField]
            List of OPItemField objects to associate with the item.
            NOTE: If the fields are from an exisiting item, and the field IDs are UUIDs, the field IDs will be regenerated
        sections: List[OPSection]
            List of OPSection objects to associate with the item.
            NOTE: If the sections are from an exisiting item, and the section IDs are UUIDs, the section IDs will be regenerated
        tags: List[str], optional
            A list of tags to apply to the login item template

        Raises
        ------
        ValueError
            If the port value fails validation as described above
        """

        if fields is None:  # pragma: no coverage
            fields = []
        else:
            fields = list(fields)

        if database_type:
            # label for database_type is "type"
            database_type_field = OPNewStringField(
                "type", database_type, field_id="database_type")
            fields.append(database_type_field)

        if hostname:
            # label for hostname field is "server"
            hostname_field = OPNewStringField(
                "server", hostname, field_id="hostname")
            fields.append(hostname_field)

        if port:
            port_field = OPNewNetworkPortField("port", port, field_id="port")
            fields.append(port_field)

        if sid:
            sid_field = OPNewStringField("SID", sid, field_id="sid")
            fields.append(sid_field)

        if database:
            # database name
            database_field = OPNewStringField(
                "database", database, field_id="database")
            fields.append(database_field)

        if username:
            # we don't use OPNewUsernameField because database username
            # doesn't declare a FIELD_PURPOSE = "USERNAME"
            username_field = OPNewStringField(
                "username", username, field_id="username")
            fields.append(username_field)

        if password:
            # we don't use OPNewPasswordField because database password
            # doesn't declare a FIELD_PURPOSE = "PASSWORD"
            password_field = OPNewConcealedField(
                "password", password, field_id="password")
            fields.append(password_field)

        if alias:
            alias_field = OPNewStringField("alias", alias, field_id="alias")
            fields.append(alias_field)

        if options:
            # label for options field is "database options"
            options_field = OPNewStringField(
                "database options", options, field_id="options")
            fields.append(options_field)

        super().__init__(title, fields, sections, tags)
