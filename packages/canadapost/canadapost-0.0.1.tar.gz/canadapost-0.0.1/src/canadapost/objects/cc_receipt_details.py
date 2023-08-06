from .base import CPObject, TextField


class CcReceiptDetails(CPObject):
    _name = 'cc-receipt-details'

    _fields = {
        "merchant_name": TextField('merchant-name'),
        "merchant_url": TextField('merchant-url'),
        "name_on_card": TextField('name-on-card'),
        "auth_code": TextField('auth-code'),
        "auth_timestamp": TextField('auth-timestamp'),
        "card_type": TextField('card-type'),
        "charge_amount": TextField('charge-amount'),
        "currency": TextField('currency'),
        "transaction_type": TextField('transaction-type'),
    }
