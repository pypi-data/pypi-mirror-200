# from lxml.etree import Element
from .base import CPObject, TextField, ObjectField
from .price_details import PriceDetails
from .service_standard import ServiceStandard


class PriceQuote(CPObject):
    _name = 'price-quote'

    _fields = {
        "code": TextField("service-code"),
        "name": TextField("service-name"),
        "details": ObjectField("price-details", format=PriceDetails),
        "service_standard": ObjectField(
            'service-standard', format=ServiceStandard
        ),
    }

#   def __init__(self, code, name, details, service_standard):
#       self.code = code
#       self.name = name
#       self.details = details
#       self.service_standard = service_standard
#
#   @classmethod
#   def from_xml(cls, node):
#       code = node.find('service-code').text
#       name = node.find('service-name').text
#
#       details = PriceDetails.from_xml(
#           node.find('price-details')
#       )
#
#       service_standard = ServiceStandard.from_xml(
#           node.find('service-standard')
#       )
#
#       return PriceQuote(
#           code,
#           name,
#           details,
#           service_standard
#       )
#
#   def to_xml(self):
#       elem = self.get_element()
#
#       code = Element('service-code')
#       code.text = self.code
#       elem.append(code)
#
#       name = Element('service-name')
#       name.text = self.name
#       elem.append(name)
#
#       elem.append(self.details.to_xml())
#
#       elem.append(self.service_standard.to_xml())
#
#       return elem
