from .base import BaseApi, method
from ..https import Methods

from ..objects.non_contract_shipments import NonContractShipments
from ..objects.non_contract_shipment_details import NonContractShipmentDetails
from ..objects.non_contract_shipment_info import NonContractShipmentInfo
from ..objects.non_contract_shipment_receipt import NonContractShipmentReceipt
from ..objects.non_contract_shipment_refund_request_info import (
    NonContractShipmentRefundRequestInfo
)


class NonContract(BaseApi):

    @method(
        '/rs/%(customer_no)s/ncshipment',
        'application/vnd.cpc.ncshipment-v4+xml',
        xmlns='http://www.canadapost.ca/ws/ncshipment-v4',
        method=Methods.POST
    )
    def create_shipment(self, data, ns):
        node = self.parse_xml(data)
        return NonContractShipmentInfo.from_xml(node)

    @method(
        '/rs/%(customer_no)s/ncshipment',
        'application/vnd.cpc.ncshipment-v4+xml',
        xmlns='http://www.canadapost.ca/ws/ncshipment-v4',
        method=Methods.GET
    )
    def get_shipments(self, data, ns):
        node = self.parse_xml(data)
        return NonContractShipments.from_xml(node)

    @method(
        '/rs/%(customer_no)s/ncshipment/%(shipment_id)s',
        'application/vnd.cpc.ncshipment-v4+xml',
        xmlns='http://www.canadapost.ca/ws/ncshipment-v4',
        method=Methods.GET
    )
    def get_shipment(self, data, ns):
        node = self.parse_xml(data)
        return NonContractShipmentInfo.from_xml(node)

    @method(
        '/rs/%(customer_no)s/ncshipment/%(shipment_id)s/details',
        'application/vnd.cpc.ncshipment-v4+xml',
        xmlns='http://www.canadapost.ca/ws/ncshipment-v4',
        method=Methods.GET
    )
    def get_shipment_details(self, data, ns):
        node = self.parse_xml(data)
        return NonContractShipmentDetails.from_xml(node)

    @method(
        '/rs/%(customer_no)s/ncshipment/%(shipment_id)s/receipt',
        'application/vnd.cpc.ncshipment-v4+xml',
        xmlns='http://www.canadapost.ca/ws/ncshipment-v4',
        method=Methods.GET
    )
    def get_shipment_receipt(self, data, ns):
        node = self.parse_xml(data)
        return NonContractShipmentReceipt.from_xml(node)

    @method(
        '/rs/%(customer_no)s/ncshipment/%(shipment_id)s/refund',
        'application/vnd.cpc.ncshipment-v4+xml',
        xmlns='http://www.canadapost.ca/ws/ncshipment-v4',
        method=Methods.POST
    )
    def refund(self, data, ns):
        node = self.parse_xml(data)
        return NonContractShipmentRefundRequestInfo.from_xml(node)
