from .base import CPObject, TextField


class SettlementInfo(CPObject):
    _name = 'settlement-info'

    _fields = {
        "promo_code": TextField('promo-code'),
    }
