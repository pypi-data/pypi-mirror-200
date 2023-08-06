from .base import (
    CPObject, TextField
)


class References(CPObject):
    _name = 'references'

    _fields = {
        "cost_centre": TextField('cost-centre'),
        "customer_ref_1": TextField('customer-ref-1'),
        "customer_ref_2": TextField('customer-ref-2'),
    }
