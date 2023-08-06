from .base import CPObject, CollectionField
from .option import Option


class Options(CPObject):
    _name = 'options'

    _fields = {
        'options': CollectionField('option', format=Option)
    }
