from .base import BaseApi, method
from ..https import Methods
from ..objects.price_quotes import PriceQuotes
from ..objects.services import Services
from ..objects.service import Service
from ..objects.option import Option


class Rating(BaseApi):

    @method(
        '/rs/ship/price',
        'application/vnd.cpc.ship.rate-v4+xml',
        xmlns='http://www.canadapost.ca/ws/ship/rate-v4',
        method=Methods.POST
    )
    def get_rates(self, data, ns):
        node = self.parse_xml(data)
        return PriceQuotes.from_xml(node)

    @method(
        '/rs/ship/service',
        # 'application/vnd.cpc.ship.rate-v4+xml',
        xmlns='http://www.canadapost.ca/ws/ship/rate-v4',
        headers={
            "Accept": "application/vnd.cpc.ship.rate-v4+xml"
        },
        method=Methods.GET,
    )
    def get_services(self, data, ns):
        node = self.parse_xml(data)
        return Services.from_xml(node)

    @method(
        '/rs/ship/service/%(service)s',
        'application/vnd.cpc.ship.rate-v4+xml',
        xmlns='application/vnd.cpc.ship.rate-v4+xml',
        method=Methods.GET
    )
    def get_service(self, data, ns):
        node = self.parse_xml(data)
        return Service.from_xml(node)

    @method(
        '/rs/ship/option/%(option)s',
        'application/vnd.cpc.ship.rate-v4+xml',
        xmlns='application/vnd.cpc.ship.rate-v4+xml',
        method=Methods.GET
    )
    def get_option(self, data, ns):
        node = self.parse_xml(data)
        return Option.from_xml(node)
