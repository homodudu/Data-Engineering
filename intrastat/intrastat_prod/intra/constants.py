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
    XML_OBJECT_TEST_OK = '_resources/eurofxref-hist-90d_test_ok.xml'
    XML_OBJECT_TEST_FAIL = '_resources/eurofxref-hist-90d_test_fail.xml'
    XML_PARSE_COLUMNS_EXP = ['Date','Currency', 'Rate']
    FX_DATA_TEST_OK = [['2022-12-30','EUR','1.00'],
                       ['2022-12-31','EUR','1.00'],
                       ['2023-01-01','EUR','1.00'],
                       ['2023-01-02','EUR','1.00'],
                       ['2023-01-03','EUR','1.00'],
                       ['2023-01-04','EUR','1.00'],
                       ['2023-01-05','EUR','1.00'],
                       ['2023-01-06','EUR','1.00']]
