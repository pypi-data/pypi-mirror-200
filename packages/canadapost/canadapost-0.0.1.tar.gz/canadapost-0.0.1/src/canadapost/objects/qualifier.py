from .base import CPObject, TextField, BooleanField


class Qualifier(CPObject):
    _name = 'qualifier'

    _fields = {
        "percent": TextField('percent'),
        "included": BooleanField('included'),
    }
