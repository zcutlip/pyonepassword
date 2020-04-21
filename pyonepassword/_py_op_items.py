from abc import ABC, abstractmethod


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
