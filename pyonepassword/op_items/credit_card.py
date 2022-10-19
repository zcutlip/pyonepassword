from ._item_descriptor_base import OPAbstractItemDescriptor
from ._item_descriptor_registry import op_register_item_descriptor_type
from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem
from .item_field_base import OPItemField
from .item_section import OPSection


@op_register_item_descriptor_type
class OPCreditCardItemDescriptor(OPAbstractItemDescriptor):
    CATEGORY = "CREDIT_CARD"

    def __init__(self, item_dict):
        super().__init__(item_dict)


@op_register_item_type
class OPCreditCardItem(OPAbstractItem):
    CATEGORY = "CREDIT_CARD"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    def additional_details(self) -> OPSection:
        details = self.sections_by_label("Additional Details")[0]
        return details

    def addl_details_item(self, field_label: str):
        details = self.additional_details()
        item_value = self._details_item(details, field_label)
        return item_value

    @property
    def credit_card_number(self):
        ccnum = self.field_value_by_id("ccnum")
        return ccnum

    @property
    def cvv(self):
        ccv = self.field_value_by_id("cvv")
        return ccv

    @property
    def expiry_date(self) -> int:
        exp_date = self.field_value_by_id("expiry")
        exp_date = int(exp_date)
        return exp_date

    @property
    def valid_from(self) -> int:
        valid_from = self.field_value_by_id("validFrom")
        valid_from = int(valid_from)
        return valid_from

    @property
    def pin(self):
        pin = self.field_value_by_id("pin")
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
        item_field: OPItemField = details.fields_by_label(field_label)[0]
        item_value = item_field.value
        return item_value
