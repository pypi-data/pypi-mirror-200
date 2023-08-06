from .base import CPObject, TextField, ObjectField, CollectionField

from .parcel_characteristics import ParcelCharacteristics
from .options import Option
from .destination import Destination
from .sender import Sender
from .recipient import Recipient
from .notification import Notification
from .references import References
from .preferences import Preferences
from .customs import Customs
from .settlement_info import SettlementInfo
from .cod_remittance import CodRemittance


class DeliverySpec(CPObject):
    _name = 'delivery-spec'

    _fields = {
        "service_code": TextField("service-code"),
        "sender": ObjectField(
            'sender', format=Sender
        ),
        "destination": ObjectField(
            'destination', format=Destination
        ),
        "recipient": ObjectField(
            'recipient', format=Recipient
        ),
        "options": CollectionField(
            'options', child_name='option', format=Option
        ),
        "parcel_characteristics": ObjectField(
            'parcel-characteristics', format=ParcelCharacteristics
        ),
        "notification": ObjectField(
            'notification', format=Notification
        ),
        "preferences": ObjectField(
            'preferences', format=Preferences
        ),
        "references": ObjectField(
            'references', format=References,
        ),
        "customs": ObjectField(
            'customs', format=Customs,
        ),
        "settlement_info": ObjectField(
            'settlement-info', format=SettlementInfo,
        ),
        "cod_remittance": ObjectField(
            'cod-remittance', format=CodRemittance,
        ),
    }
