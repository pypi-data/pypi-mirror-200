from .base import (
    CPObject,
    TextField,
    CollectionField,
    ObjectField,
    BooleanField,
    RangeField
)
from .dimensional_restrictions import DimensionalRestrictions
from .option import Option


class Restrictions(CPObject):
    _name = 'restrictions'

    _fields = {
        "weight-restriction": RangeField('weight-restriction'),
        "dimensional_restrictions": ObjectField(
            'dimensional-restrictions', format=DimensionalRestrictions
        ),
        "options": CollectionField(
            'options', child_name='option', format=Option
        ),
        "density_factor": TextField('density-factor'),
        "can_ship_in_mailing_tube": BooleanField('can-ship-in-mailing-tube'),
        "can_ship_unpackaged": BooleanField('can-ship-unpackaged'),
        "allowed_as_return_service": BooleanField('allowed-as-return-service')
    }
