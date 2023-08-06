from .base import CPObject, TextField, ObjectField, BooleanField

from .dimensions import Dimensions


class ParcelCharacteristics(CPObject):
    _name = 'parcel-characteristics'

    _fields = {
        "weight": TextField('weight'),
        "dimensions": ObjectField('dimensions', format=Dimensions),
        "document": BooleanField("document"),
        "unpackaged": BooleanField("unpackaged"),
        "mailing_tube": BooleanField("mailing-tube"),
    }
