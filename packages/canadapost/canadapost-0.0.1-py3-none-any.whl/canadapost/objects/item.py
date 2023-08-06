from .base import CPObject, TextField 


class Item(CPObject):
    _name = 'item'

    _fields = {
        "sku": TextField('sku'),
        "description": TextField('customs-description'),
        "number_of_units": TextField('customs-number-of-units'),
        "value_per_unit": TextField('customs-value-per-unit'),
        "unit_of_measure": TextField('customs-unit-of-measure'),
        "hs_tariff_code": TextField('hs-tariff-code'),
        "unit_weight": TextField('unit-weight'),
        "country_of_origin": TextField('country-of-origin'),
        "provice_of_origin": TextField('province-of-origin'),
    }
