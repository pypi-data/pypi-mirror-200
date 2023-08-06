from .base import CPObject, TextField


class NonContractShipmentRefundRequest(CPObject):
    _name = 'non-contract-shipment-refund-request'
    _xmlns = 'http://www.canadapost.ca/ws/ncshipment-v4'

    _fields = {
        "email": TextField("email"),
    }
