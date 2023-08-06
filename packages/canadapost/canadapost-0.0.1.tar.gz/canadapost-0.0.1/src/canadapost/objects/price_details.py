# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from .base import CPObject, TextField, ObjectField, CollectionField
from .taxes import Taxes
from .option import Option
from .adjustment import Adjustment


class PriceDetails(CPObject):
    _name = 'price-details'

    _fields = {
        "base": TextField('base', format=float),
        "due": TextField('due', format=float),
        "taxes": ObjectField('taxes', format=Taxes),
        "options": CollectionField(
            'options', child_name='option', format=Option
        ),
        "adjustments": CollectionField(
            'adjustments', child_name='adjustment', format=Adjustment
        ),
    }

#   def __init__(self, base, due, taxes, options, adjustments):
#       self.base = base
#       self.due = due
#       self.taxes = taxes
#       self.options = options
#       self.adjustments = adjustments
#
#   @classmethod
#   def from_xml(cls, node):
#       base = float(node.xpath('//base')[0].text),
#       due = float(node.xpath('//due')[0].text),
#       taxes = Taxes.from_xml(node.find('taxes')),
#       options = Options.from_xml(node.find('options'))
#       adjustments = Adjustments.from_xml(node.find('adjustments'))
#
#       return PriceDetails(
#           base,
#           due,
#           taxes,
#           options,
#           adjustments
#       )
#
#   def to_xml(self):
#       elem = self.get_element()
#
#       elem.append(self.adjustments.to_xml())
#
#       return elem
