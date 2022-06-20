from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem

# {
#     "id": "2dvgl7kk5yjrq3gxwqimp5awve",
#     "title": "Example Password",
#     "version": 1,
#     "vault": {
#         "id": "gshlsjsajnawtnjynzgwmiebge",
#         "name": "Test Data"
#     },
#     "category": "PASSWORD",
#     "last_edited_by": "5GHHPJK5HZC5BAT7WDUXW57G44",
#     "created_at": "2021-11-23T05:46:01Z",
#     "updated_at": "2021-11-23T05:46:01Z",
#     "additional_information": "2021-11-22 09:46 PM",
#     "fields": [
#         {
#             "id": "password",
#             "type": "CONCEALED",
#             "purpose": "PASSWORD",
#             "label": "password",
#             "value": "iXdx8KAEmUkPqCvHHYjngHzRr7",
#             "reference": "op://Test Data/Example Password/password",
#             "password_details": {
#                 "strength": "FANTASTIC"
#             }
#         },
#         {
#             "id": "notesPlain",
#             "type": "STRING",
#             "purpose": "NOTES",
#             "label": "notesPlain",
#             "reference": "op://Test Data/Example Password/notesPlain"
#         }
#     ]
# }


@op_register_item_descriptor_type
class OPPasswordItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "PASSWORD"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPPasswordItem(OPAbstractItem):
    CATEGORY = "PASSWORD"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def password(self):
        password = self.field_value_by_id("password")
        return password
