from lxml.etree import Element
from .base import CPObject, TextField, DateField, ObjectField, CollectionField
from datetime import datetime

from .services import Service
from .parcel_characteristics import ParcelCharacteristics
from .options import Option
from .destination import Destination


class MailingScenario(CPObject):
    _name = 'mailing-scenario'

    _xmlns = 'http://www.canadapost.ca/ws/ship/rate-v4'

    _fields = {
        "customer_number": TextField("customer-number"),
        "contract_id": TextField("contract-id"),
        "promo_code": TextField("promo-code"),
        "quote_type": TextField("quote-type"),
        "expected_mailing_date": DateField(
            "expected-mailing-date", format='%Y-%m-%d'
        ),
        "origin_postal_code": TextField("origin-postal-code"),
        "options": CollectionField(
            'options', child_name='option', format=Option
        ),
        "parcel_characteristics": ObjectField(
            'parcel-characteristics', format=ParcelCharacteristics
        ),
        "services": CollectionField(
            'services', child_name='service', format=Service
        ),
        "destination": ObjectField('destination', format=Destination)
    }
