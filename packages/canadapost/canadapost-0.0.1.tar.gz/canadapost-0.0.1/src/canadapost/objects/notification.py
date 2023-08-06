from .base import (
    CPObject, TextField, BooleanField
)


class Notification(CPObject):
    _name = 'notification'

    _fields = {
        "email": TextField('email'),
        "on_shipment": BooleanField('on-shipment'),
        "on_exception": BooleanField('on-exception'),
        "on_delivery": BooleanField('on-delivery'),
    }
