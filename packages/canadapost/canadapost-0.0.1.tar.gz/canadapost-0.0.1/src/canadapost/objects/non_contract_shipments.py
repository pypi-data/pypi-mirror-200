from .base import CPObject, TextField, CollectionField, LinksField


class NonContractShipments(CPObject):
    _name = 'non-contract-shipments'

    _xmlns = 'http://www.canadapost.ca/ws/ncshipment-v4'

    _fields = {
        'id': TextField('shipment-id'),
        'tracking_pin': TextField('tracking-pin'),
        'links': CollectionField(
            'link', field_type=LinksField
        )
    }
