"""
File to store constants
"""

#from enum import Enum

class CommodityCodes(str):
    """
    Global variables for commodity_codes class.
    """

    URL_USE = 'https://www.cbs.nl/-/media/cbsvooruwbedrijf/international-trade-in-goods/commoditycodes-2023.xlsx'
    URL_TEST = 'https://www.cbs.nl/-/media/cbsvooruwbedrijf/international-trade-in-goods/commoditycodes-XXXX.xlsx'

class FxRates(str):

    """
    Global variables for commodity_codes class.
    """

    URL_USE = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
    URL_TEST = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-XXd.xml'
    XML_NAMESPACES = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    XML_CHILD = './/ex:Cube'
