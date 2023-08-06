from .base import CPObject, CollectionField
from .adjustment import Adjustment


class Adjustments(CPObject):
    _name = 'adjustments'

    _fields = {
        "adjustments": CollectionField('adjustment', format=Adjustment),
    }

#   def __init__(self, adjustments):
#       self.adjustments = {
#           adjustment.code: adjustment
#           for adjustment in adjustments
#       }
#
#   @classmethod
#   def from_xml(cls, node):
#       adjustments = [
#           Adjustment.from_xml(adjustment)
#           for adjustment in node.xpath('.//adjustment')
#       ]
#
#       return Adjustments(adjustments)
#
#   def to_xml(self):
#       elem = self.get_element()
#
#       for adjustment in self.adjustments.values():
#           elem.append(adjustment.to_xml())
#
#       return elem
