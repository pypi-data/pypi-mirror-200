from .base import CPObject, TextField, ObjectField

from .delivery_spec import DeliverySpec


class NonContractShipment(CPObject):
    _name = 'non-contract-shipment'

    _xmlns = 'http://www.canadapost.ca/ws/ncshipment-v4'

    _fields = {
        'requested_shipping_point': TextField('requested-shipping-point'),
        'delivery_spec': ObjectField('delivery-spec', format=DeliverySpec),
    }
