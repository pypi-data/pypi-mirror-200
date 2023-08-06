from .base import (
    CPObject, TextField, ObjectField, BooleanField, LinkField, CollectionField
)
from .qualifier import Qualifier


class Option(CPObject):
    _name = 'option'

    _fields = {
        "code": TextField('option-code'),
        "name": TextField('option-name'),
        "price": TextField('option-price'),
        "amount": TextField('option-amount'),
        "qualifier_1": BooleanField('option-qualifier-1'),
        "qualifier_2": TextField('option-qualifier-2'),

        "qualifier": ObjectField('qualifier', format=Qualifier),
        "qualifier_required": BooleanField('qualifier-required'),
        "mandatory": BooleanField("mandatory"),
        "prints_on_label": BooleanField("prints-on-label"),
        "qualifier_max": TextField("qualifier-max"),
        "option": LinkField('option'),
        "option_class": TextField("option-class"),
        "conflicting_options": CollectionField(
            'conflicting-options',
            child_name='option-code',
            field_type=TextField
        ),
        "prerequisite_options": CollectionField(
            'prerequisite-options',
            child_name='option-code',
            field_type=TextField
        )
    }
