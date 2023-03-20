from typing import Union

from .._item_descriptor_registry import op_register_item_descriptor_type
from .._item_type_registry import op_register_item_type
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
