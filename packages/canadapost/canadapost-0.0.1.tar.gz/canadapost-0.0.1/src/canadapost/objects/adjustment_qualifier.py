from .base import CPObject, TextField, BooleanField


class AdjustmentQualifier(CPObject):
    _name = 'adjustment-qualifier'

    _fields = {
        "percent": TextField('percent'),
        "included": BooleanField('included'),
    }
