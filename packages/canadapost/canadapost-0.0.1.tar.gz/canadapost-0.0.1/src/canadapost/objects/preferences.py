from .base import (
    CPObject, TextField, BooleanField
)


class Preferences(CPObject):
    _name = 'preferences'

    _fields = {
        "email": TextField('email'),
        "show_packing_instructions": BooleanField('show-packing-instructions'),
        "show_postage_rate": BooleanField('show-postage-rate'),
        "show_insured_value": BooleanField('show-insured-value'),
    }
