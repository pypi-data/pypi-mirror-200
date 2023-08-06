from lxml import etree

import pytest
from fixtures import *


def test_client(canadapost_sync_client):
    assert hasattr(canadapost_sync_client, 'send_request') is True


def test_rating_api(canadapost_sync_client, rating_api):
    assert hasattr(rating_api, 'get_rates') is True
    assert hasattr(rating_api, 'get_services') is True
    assert hasattr(rating_api, 'get_service') is True
    assert hasattr(rating_api, 'get_option') is True
    assert canadapost_sync_client == rating_api.client


def test_get_rates(rating_api):
    from canadapost.objects.mailing_scenario import MailingScenario
    from canadapost.objects.destination import Destination
    from canadapost.objects.domestic import Domestic
    from canadapost.objects.price_quotes import PriceQuotes
    from canadapost.objects.price_quote import PriceQuote
    from canadapost.objects.parcel_characteristics import ParcelCharacteristics

    scenario = MailingScenario(
        customer_number=rating_api.client.customer_no,
        parcel_characteristics=ParcelCharacteristics(
            weight=1,
        ),
        origin_postal_code='K2B8J6',
        destination=Destination(
            domestic=Domestic(
                postal_code='J0E1X0',
            ),
        )
    )

    rates = rating_api.get_rates(
        etree.tostring(scenario.to_xml(set_xmlns=True)).decode()
    )

    assert isinstance(rates, PriceQuotes) is True
    assert len(rates.quotes) > 0
    assert isinstance(rates.quotes[0], PriceQuote) is True


def test_get_services(rating_api):
    from canadapost.objects.services import Services
    from canadapost.objects.service import Service

    services = rating_api.get_services()

    assert isinstance(services, Services) is True
    assert len(services.services) > 0

    assert services.services[0].code is not None

    service = rating_api.get_service(
        params={
            "service": services.services[0].code
        }
    )

    assert isinstance(service, Service) is True
    assert service.code == services.services[0].code


def test_get_option(rating_api):
    from canadapost.objects.option import Option

    option = rating_api.get_option(
        params={
            "option": "RTS"
        }
    )

    assert isinstance(option, Option)
    assert option.code == 'RTS'
