from lxml import etree

import pytest
from fixtures import *
from datetime import datetime


def test_create_shipment(non_contract_api):
    from canadapost.objects.non_contract_shipment import NonContractShipment
    from canadapost.objects.non_contract_shipment_info import (
        NonContractShipmentInfo
    )
    from canadapost.objects.delivery_spec import DeliverySpec
    from canadapost.objects.destination import Destination
    from canadapost.objects.sender import Sender
    from canadapost.objects.address_details import AddressDetails
    from canadapost.objects.parcel_characteristics import ParcelCharacteristics
    from canadapost.objects.preferences import Preferences

    shipment = NonContractShipment(
        delivery_spec=DeliverySpec(
            service_code='DOM.RP',
            sender=Sender(
                company='Canada Post',
                contact_phone='',
                address_details=AddressDetails(
                    line_1='1000 3e Ave',
                    city='Québec',
                    prov_state='QC',
                    postal_zip_code='G1L2X0'
                )
            ),
            destination=Destination(
                name='Montréal',
                address_details=AddressDetails(
                    line_1='2000 Boulevard Marcel-Laurin',
                    city='Saint-Laurent',
                    prov_state='QC',
                    postal_zip_code='H4R1J0',
                    country_code='CA',
                )
            ),
            parcel_characteristics=ParcelCharacteristics(
                weight=1
            ),
            preferences=Preferences(
                show_packing_instructions=True
            ),
        )
    )

    shipment_info = non_contract_api.create_shipment(
        etree.tostring(shipment.to_xml(set_xmlns=True)).decode(),
    )

    assert isinstance(shipment_info, NonContractShipmentInfo) is True


def test_get_shipments_by_tracking_pin(non_contract_api):
    from canadapost.objects.non_contract_shipments import NonContractShipments

    test_pin = "123456789012"

    shipments = non_contract_api.get_shipments(
        params={
            "trackingPIN": test_pin
        }
    )

    assert isinstance(shipments, NonContractShipments) is True
    assert len(shipments.links) == 1
    assert shipments.links[0].get('rel') == 'shipment'


def test_get_shipments_by_date(non_contract_api):
    from canadapost.objects.non_contract_shipments import NonContractShipments

    shipments = non_contract_api.get_shipments(
        params={
            "from": "202001010100"
        }
    )

    assert isinstance(shipments, NonContractShipments) is True

    assert len(shipments.links) > 1
    for link in shipments.links:
        assert link.get('rel') == 'shipment'
        assert link.get('href') is not None
        assert len(link.get('href')) > 0


def test_get_shipment_details(non_contract_api):
    from canadapost.objects.non_contract_shipment_details import (
        NonContractShipmentDetails
    )
    test_pin = "123456789012"

    shipment_links = non_contract_api.get_shipments(
        params={
            "trackingPIN": test_pin
        }
    )

    shipment_url = shipment_links.links[0].get('href')
    shipment_id = shipment_url.split('/')[-1]

    shipment_details = non_contract_api.get_shipment_details(
        params={
            "shipment_id": shipment_id
        }
    )

    assert isinstance(shipment_details, NonContractShipmentDetails) is True


def test_get_shipment(non_contract_api):
    from canadapost.objects.non_contract_shipment_info import (
        NonContractShipmentInfo
    )
    test_pin = "123456789012"

    shipment_links = non_contract_api.get_shipments(
        params={
            "trackingPIN": test_pin
        }
    )

    shipment_url = shipment_links.links[0].get('href')
    shipment_id = shipment_url.split('/')[-1]

    shipment_details = non_contract_api.get_shipment(
        params={
            "shipment_id": shipment_id
        }
    )

    assert isinstance(shipment_details, NonContractShipmentInfo) is True


def test_get_shipment_refund(non_contract_api):
    from canadapost.objects.non_contract_shipment_refund_request import (
        NonContractShipmentRefundRequest
    )
    from canadapost.objects.non_contract_shipment_refund_request_info import (
        NonContractShipmentRefundRequestInfo
    )
    test_pin = "123456789012"

    shipment_links = non_contract_api.get_shipments(
        params={
            "trackingPIN": test_pin
        }
    )

    shipment_url = shipment_links.links[0].get('href')
    shipment_id = shipment_url.split('/')[-1]

    refund = NonContractShipmentRefundRequest(
        email="name@example.com"
    )

    refund_info = non_contract_api.refund(
        data=etree.tostring(refund.to_xml(set_xmlns=True)).decode(),
        params={
            "shipment_id": shipment_id
        }
    )
    RefundInfo = NonContractShipmentRefundRequestInfo
    assert isinstance(refund_info, RefundInfo) is True
    assert refund_info.id == '0123456789'
    assert refund_info.date == datetime.now().strftime('%Y-%m-%d')
