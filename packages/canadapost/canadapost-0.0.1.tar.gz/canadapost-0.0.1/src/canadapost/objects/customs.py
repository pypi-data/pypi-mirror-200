from .base import CPObject, TextField, CollectionField
from .item import Item


class Customs(CPObject):
    _name = 'customs'

    _fields = {
        "currency": TextField('currency'),
        "conversion_from_cad": TextField('conversion-from-cad'),
        "reason-for-export": TextField('reason-for-export'),
        "other_reason": TextField('other-reason'),
        # unused
        "duties_and_taxes_prepaid": TextField('duties-and-taxes-prepaid'),
        "certificate_number": TextField('certificate-number'),
        "licence_number": TextField('licence-number'),
        "invoice_number": TextField('invoice-number'),
        "sku-list": CollectionField(
            "sku-list", child_name='item', format=Item
        ),
    }
