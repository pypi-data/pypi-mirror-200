from .base import CPObject, TextField, ObjectField
from .delivery_spec import DeliverySpec


class NonContractShipmentDetails(CPObject):
    """
    Response type of get_shipment_details on NonContract API
    """
    _name = 'non-contract-shipment-details'

    _xmlns = 'http://www.canadapost.ca/ws/ncshipment-v4'

    _fields = {
        'final_shipping_point': TextField('final-shipping-point'),
        'tracking_pin': TextField('tracking-pin'),
        'delivery_spec': ObjectField('delivery-spec', format=DeliverySpec),
    }
