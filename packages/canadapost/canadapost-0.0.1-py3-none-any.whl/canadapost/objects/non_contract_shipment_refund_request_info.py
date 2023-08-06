from .base import CPObject, TextField


class NonContractShipmentRefundRequestInfo(CPObject):
    _name = 'non-contract-shipment-refund-request-info'

    _fields = {
        "id": TextField("service-ticket-id"),
        "date": TextField("service-ticket-date"),
    }
