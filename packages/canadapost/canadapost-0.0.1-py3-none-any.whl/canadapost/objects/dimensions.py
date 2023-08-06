from .base import CPObject, TextField


class Dimensions(CPObject):
    _name = 'dimensions'

    _fields = {
        "width": TextField('width'),
        "height": TextField('height'),
        "length": TextField('length'),
    }
