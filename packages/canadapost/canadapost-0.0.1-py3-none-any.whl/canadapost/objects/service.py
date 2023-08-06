from .base import CPObject, TextField, LinkField, CollectionField, ObjectField
from .option import Option
from .restrictions import Restrictions


class Service(CPObject):
    _name = 'service'

    _fields = {
        "code": TextField('service-code'),
        "name": TextField('service-name'),
        "link": LinkField('service'),
        "comment": TextField('comment'),
        "options": CollectionField(
            'options', child_name='option', format=Option
        ),
        "restrictions": ObjectField('restrictions', format=Restrictions)
    }
