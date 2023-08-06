from .base import CPObject, TextField, ObjectField
from .domestic import Domestic
from .address_details import AddressDetails


class Destination(CPObject):
    _name = 'destination'

    _fields = {
        # NonContractShipping
        "name": TextField("name"),
        "company": TextField("company"),
        "additional_addess_info": TextField("additional-addess-info"),
        "client_voice_number": TextField("client-voice-number"),
        "address_details": ObjectField(
            "address-details", format=AddressDetails
        ),
        # Rating
        "domestic": ObjectField('domestic', format=Domestic),
    }
