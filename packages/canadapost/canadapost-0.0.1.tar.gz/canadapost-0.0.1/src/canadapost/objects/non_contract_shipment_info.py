from .base import CPObject, TextField, CollectionField, LinksField


class NonContractShipmentInfo(CPObject):
    _name = 'non-contract-shipment-info'

    _xmlns = 'http://www.canadapost.ca/ws/ncshipment-v4'

    _fields = {
        'id': TextField('shipment-id'),
        'tracking_pin': TextField('tracking-pin'),
        'links': CollectionField(
            'links', child_name='link', field_type=LinksField
        )
    }
