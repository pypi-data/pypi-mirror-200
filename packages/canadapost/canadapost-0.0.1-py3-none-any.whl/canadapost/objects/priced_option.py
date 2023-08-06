from .base import CPObject, TextField


class PricedOption(CPObject):
    _name = 'priced-option'

    _fields = {
        "code": TextField('option-code'),
        "price": TextField('option-price'),
    }
