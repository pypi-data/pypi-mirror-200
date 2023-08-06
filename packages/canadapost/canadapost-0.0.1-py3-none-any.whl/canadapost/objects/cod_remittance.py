from .base import CPObject, TextField, ObjectField
from .address_details import AddressDetails


class CodRemittance(CPObject):
    _name = 'cod-remittance'

    _fields = {
        "name": TextField("name"),
        "company": TextField("company"),
        "address_details": ObjectField(
            "address-details", format=AddressDetails
        ),
    }
