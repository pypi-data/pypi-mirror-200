from lxml.etree import Element

from .base import CPObject, TextField, ObjectField


class Domestic(CPObject):
    _name = 'domestic'

    _fields = {
        "postal_code": TextField('postal-code'),
    }
