from ._op_item_type_registry import op_register_item_type
from ._op_items_base import OPAbstractItem
from .item_section import OPSection, OPSectionField

@op_register_item_type
class OPCreditCardItem(OPAbstractItem):
    TEMPLATE_ID = "002"

    def __init__(self, item_dict):
        super().__init__(item_dict)

    def credit_card_details(self) -> OPSection:
        details = self.first_section
        return details

    def additional_details(self) -> OPSection:
        details = self.sections_by_title("Additional Details")[0]
        return details

    def primary_details_item(self, field_label: str):
        details = self.credit_card_details()
        item_value = self._details_item(details, field_label)
        return item_value

    def addl_details_item(self, field_label: str):
        details = self.additional_details()
        item_value = self._details_item(details, field_label)
        return item_value

    @property
    def credit_card_number(self):
        ccnum = self.primary_details_item("number")
        return ccnum

    @property
    def cvv(self):
        ccv = self.primary_details_item("verification number")
        return ccv

    @property
    def expiry_date(self) -> int:
        exp_date = self.primary_details_item("expiry date")
        return exp_date

    @property
    def valid_from(self) -> int:
        valid_from = self.primary_details_item("valid from")
        return valid_from

    @property
    def pin(self):
        pin = self.addl_details_item("PIN")
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
        item_field: OPSectionField = details.fields_by_label(field_label)[0]
        item_value = item_field.value
        return item_value
