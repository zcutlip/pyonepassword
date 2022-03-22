from ._item_descriptor_base import OPAbstractItemDescriptor
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem, OPItemTemplateMixin, OPMutableItemOverview
from ._item_descriptor_registry import op_register_item_descriptor_type


@op_register_item_descriptor_type
class OPLoginDescriptorItem(OPAbstractItemDescriptor):
    TEMPLATE_ID = "001"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPLoginItem(OPAbstractItem):
    TEMPLATE_ID = "001"
    ITEM_CATEGORY = "Login"

    def __init__(self, item_dict, **kwargs):
        super().__init__(item_dict, **kwargs)

    def get_details_subfield(self, subfield_designation):
        """
        "details": {
            "fields": [
            {
                "designation": "password",
                "name": "password",
                "type": "P",
                "value": "doth-parrot-hid-tussock-veldt"
            },
            {
                "designation": "username",
                "name": "username",
                "type": "T",
                "value": "zcutlip"
            }
            ],
            "notesPlain": ""
        }
        """
        subfields = self.get_details_value("fields")
        field = None
        for f in subfields:
            if f["designation"] == subfield_designation:
                field = f
                break
        return field

    def get_details_subfield_value(self, field_designation):
        field_value = None
        field = self.get_details_subfield(field_designation)
        field_value = field["value"]
        return field_value

    @property
    def username(self):
        username = self.get_details_subfield_value("username")
        return username

    @username.setter
    def username(self, username: str):
        username_field = self.get_details_subfield("username")
        username_field["value"] = username

    @property
    def password(self):
        password = self.get_details_subfield_value("password")
        return password

    @password.setter
    def password(self, password: str):
        password_field = self.get_details_subfield("password")
        password_field["value"] = password


class OPLoginItemTemplate(OPItemTemplateMixin, OPLoginItem):
    TEMPLATE_ID = OPLoginItem.TEMPLATE_ID

    def __init__(self,  username, password, *args, url=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = username
        self.password = password
        # replace overview with a modifiable overview
        self._overview = OPMutableItemOverview(self._overview)
        self._overview.set_url(url)
