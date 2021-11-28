from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem

# {
#     "uuid": "2dvgl7kk5yjrq3gxwqimp5awve",
#     "templateUuid": "005",
#     "trashed": "N",
#     "createdAt": "2021-11-23T05:46:01Z",
#     "updatedAt": "2021-11-23T05:46:01Z",
#     "changerUuid": "RAXCWKNRRNGL7I3KSZOH5ERLHI",
#     "itemVersion": 1,
#     "vaultUuid": "yhdg6ovhkjcfhn3u25cp2bnl6e",
#     "details": {
#         "notesPlain": "",
#         "password": "iXdx8KAEmUkPqCvHHYjngHzRr7",
#         "passwordHistory": [],
#         "sections": []
#     },
#     "overview": {
#         "ainfo": "2021-11-22 09:46 PM",
#         "ps": 100,
#         "title": "Example Password"
#     }
# }


@op_register_item_type
class OPPasswordItem(OPAbstractItem):
    TEMPLATE_ID = "005"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    @property
    def password(self):
        password = self.get_details_value("password")
        return password
