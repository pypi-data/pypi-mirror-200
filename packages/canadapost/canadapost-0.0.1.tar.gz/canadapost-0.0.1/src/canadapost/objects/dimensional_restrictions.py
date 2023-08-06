from .base import CPObject, TextField, ObjectField, BooleanField, RangeField
from .qualifier import Qualifier


class DimensionalRestrictions(CPObject):
    _name = 'dimensional-restrictions'

    _fields = {
        "length": RangeField('length'),
        "width": RangeField('width'),
        "height": RangeField('height'),
        "length_plus_girth_max": TextField("length-plus-girth-max"),
        "overize_limit": TextField("oversize-limit"),
    }
