from .base import CPObject, CollectionField
from .price_quote import PriceQuote


class PriceQuotes(CPObject):
    _name = 'price-quotes'

    _fields = {
        "quotes": CollectionField('price-quote', format=PriceQuote),
    }
