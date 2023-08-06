from .base import CPObject, CollectionField
from .service import Service


class Services(CPObject):
    _name = 'services'

    _fields = {
        "services": CollectionField('service', format=Service)
    }

#   def __init__(self, services):
#       self.adjustments = {
#           adjustment.code: adjustment
#           for adjustment in services
#       }
#
#   @classmethod
#   def from_xml(cls, node):
#       services = []
#
#       return Services(services)
#
#   def to_xml(self):
#       elem = self.get_element()
#       return elem
