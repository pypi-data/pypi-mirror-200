from .base import CPObject, TextField, ObjectField
from .adjustment_qualifier import AdjustmentQualifier


class Adjustment(CPObject):
    _name = 'adjustment'

    _fields = {
        "code": TextField('adjustment-code'),
        "name": TextField('adjustment-name'),
        "qualifier": ObjectField(
            'adjustment-qualifier', format=AdjustmentQualifier
        ),
    }
