from .base import CPObject, TextField, ObjectField, CollectionField

from .adjustment import Adjustment
from .cc_receipt_details import CcReceiptDetails
from .priced_option import PricedOption
from .service_standard import ServiceStandard


class NonContractShipmentReceipt(CPObject):
    _name = 'non-contract-shipment-receipt'

    _fields = {
        "final_shipping_point": TextField("final-shipping-point"),
        "shipping_point_name": TextField("shipping-point-name"),
        "shipping_point_id": TextField("shipping-point-id"),
        "mailed_by_customer": TextField("mailed-by-customer"),
        "cc_receipt_details": ObjectField(
            "cc-receipt-details", format=CcReceiptDetails
        ),
        "service_code": TextField("service-code"),
        "base_amount": TextField("base-amount"),
        "priced_options": CollectionField(
            "priced-options", child_name="priced-option", format=PricedOption
        ),
        "adjustments": CollectionField(
            "adjustments", child_name="adjustment", format=Adjustment
        ),
        "pre_tax_amount": TextField("pre-tax-amount"),
        "gst_amount": TextField("gst-amount"),
        "pst_amount": TextField("pst-amount"),
        "hst_amount": TextField("hst-amount"),
        "service_standard": ObjectField(
            "service-standard", format=ServiceStandard
        ),
        "rated_weight": TextField("rated-weight"),
    }
