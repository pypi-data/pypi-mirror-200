from .base import CPObject, BooleanField, TextField, DateField
# from lxml.etree import Element
# from datetime import datetime


class ServiceStandard(CPObject):
    _name = 'service-standard'

    _fields = {
        "am_delivery": BooleanField('am-delivery'),
        "guaranteed_delivery": BooleanField('guaranteed-delivery'),
        "expected_transit_time": TextField('expected-transit-time'),
        "expected_delivery_date": DateField(
            'expected-delivery-date', format='%Y-%m-%d'
        ),
    }

#   def __init__(
#       self,
#       am_delivery,
#       guaranteed_delivery,
#       expected_transit_time,
#       expected_delivery_date
#   ):
#       self.am_delivery = am_delivery
#       self.guaranteed_delivery = guaranteed_delivery
#       self.expected_transit_time = expected_transit_time
#       self.expected_delivery_date = expected_delivery_date
#
#   @classmethod
#   def from_xml(cls, node):
#       am_delivery = node.find('am-delivery').text
#       am_delivery = am_delivery == 'true'
#
#       guaranteed_delivery = node.find('guaranteed-delivery').text
#       guaranteed_delivery = guaranteed_delivery == 'true'
#
#       expected_transit_time = node.find('expected-transit-time').text
#       expected_transit_time = float(
#           expected_transit_time
#       )
#
#       expected_delivery_date = node.find('expected-delivery-date').text
#       expected_delivery_date = datetime.strptime(
#           expected_delivery_date, '%Y-%m-%d'
#       )
#
#       return ServiceStandard(
#           am_delivery,
#           guaranteed_delivery,
#           expected_transit_time,
#           expected_delivery_date
#       )
#
#   def to_xml(self):
#       elem = self.get_element()
#
#       am_delivery = Element('am-delivery')
#       am_delivery.text = 'true' if self.am_delivery else 'false'
#
#       guaranteed_delivery = Element('guaranteed-delivery')
#       guaranteed_delivery.text = (
#           'true'
#           if self.guaranteed_delivery
#           else 'false'
#       )
#
#       expected_transit_time = Element('expected-transit-time')
#       expected_transit_time.text = str(self.expected_transit_time)
#
#       expected_delivery_date = Element('expected-delivery-date')
#       expected_delivery_date.text = self.expected_delivery_date.strftime(
#           '%Y-%m-%d'
#       )
#
#       elem.append(am_delivery)
#       elem.append(guaranteed_delivery)
#       elem.append(expected_transit_time)
#       elem.append(expected_delivery_date)
#
#       return elem
