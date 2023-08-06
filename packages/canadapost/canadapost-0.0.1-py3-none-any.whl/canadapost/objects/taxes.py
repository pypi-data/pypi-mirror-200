from .base import CPObject, TextField


class Taxes(CPObject):
    _name = 'taxes'

    _fields = {
        'gst': TextField('gst'),
        'hst': TextField('hst'),
        'pst': TextField('pst'),
    }

#   def __init__(self, gst, gst_percent, pst, hst):
#       self.gst = gst
#       self.gst_percent = gst_percent
#       self.pst = pst
#       self.hst = hst
#
#   @classmethod
#   def from_xml(cls, node):
#       gst = CPObject.get_float(node, 'gst')
#       gst_node = node.find('gst')
#
#       if 'percent' in gst_node.attrib:
#           gst_percent = float(gst_node.attrib['percent'])
#       else:
#           gst_percent = None
#
#       hst = CPObject.get_float(node, 'hst')
#       pst = CPObject.get_float(node, 'pst')
#
#       return Taxes(
#           gst,
#           gst_percent,
#           pst,
#           hst
#       )
