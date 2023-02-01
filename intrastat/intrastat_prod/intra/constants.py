"""
File to store constants
"""
class CommodityCodes(str):
    """
    Global variables for commodity_codes class.
    """

    URL_EXP = 'https://www.cbs.nl/-/media/cbsvooruwbedrijf/international-trade-in-goods/commoditycodes-2023.xlsx'
    URL_NOT_EXP = 'https://www.cbs.nl/-/media/cbsvooruwbedrijf/international-trade-in-goods/commoditycodes-XXXX.xlsx'

class FxRates(str):

    """
    Global variables for commodity_codes class.
    """

    URL_EXP = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
    URL_NOT_EXP = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-XXd.xml'
    XML_NAMESPACES = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    XML_CHILD = './/ex:Cube'
    XML_OBJECT_TEST_EXP = '_resources/eurofxref-hist-90d_test_exp.xml'
    XML_OBJECT_TEST_NOT_EXP = '_resources/eurofxref-hist-90d_test_not_exp.xml'
    FX_DATA_COLUMNS_TEST_EXP= ['Date','Currency', 'Rate']
    FX_DATA_COLUMNS_TEST_NOT_EXP = ['X','Y', 'Z']
    FX_DATA_BODY_TEST_EXP = [['2022-12-30','EUR','1.00'],
                       ['2022-12-31','EUR','1.00'],
                       ['2023-01-01','EUR','1.00'],
                       ['2023-01-02','EUR','1.00'],
                       ['2023-01-03','EUR','1.00'],
                       ['2023-01-04','EUR','1.00'],
                       ['2023-01-05','EUR','1.00'],
                       ['2023-01-06','EUR','1.00']]
