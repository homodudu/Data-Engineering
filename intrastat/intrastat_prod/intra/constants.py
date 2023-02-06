"""
File to store constants
"""
class CommodityCodes(str):
    """
    Global variables for commodity codes class.
    """
    URL_EXP = 'https://www.cbs.nl/-/media/cbsvooruwbedrijf/international-trade-in-goods/commoditycodes-2023.xlsx'
    URL_NOT_EXP = 'https://www.cbs.nl/-/media/cbsvooruwbedrijf/international-trade-in-goods/commoditycodes-XXXX.xlsx'
    COLUMNS_EXP= ['Commodity Code','SU', 'Description']
    COLUMNS_NOT_EXP = ['X','Y', 'Z']
    BODY_EXP = [['01012100','p/st','CC Description']]
    BODY_NOT_EXP = [['001012100','p/st','CC Description']]
    STR_LEN_EXP = 8
    FILENAME_EXP = 'CN8 Codes.csv'
    FILENAME_NOT_EXP = 'CN8 Codes NE.csv'

class FxRates(str):
    """
    Global variables for fx rates class.
    """
    URL_EXP = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
    URL_NOT_EXP = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-XXd.xml'
    XML_NAMESPACES_EXP = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    XML_NAMESPACES_NOT_EXP = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofXXXX'}
    XML_CHILD_EXP = './/ex:Cube'
    XML_CHILD_NOT_EXP = './/ex:XXXX'
    XML_OBJECT_EXP = '_resources/eurofxref-hist-90d_test_exp.xml'
    XML_OBJECT_NOT_EXP = '_resources/eurofxref-hist-90d_test_not_exp.xml'
    COLUMNS_EXP= ['Date','Currency', 'Rate']
    COLUMNS_NOT_EXP = ['X','Y', 'Z']
    BODY_EXP = [['2022-12-30','EUR','1.00'],
                ['2022-12-31','EUR','1.00'],
                ['2023-01-01','EUR','1.00'],
                ['2023-01-02','EUR','1.00'],
                ['2023-01-03','EUR','1.00'],
                ['2023-01-04','EUR','1.00'],
                ['2023-01-05','EUR','1.00'],
                ['2023-01-06','EUR','1.00']]
    FILENAME_EXP = 'ECB FX Rates.csv'
    FILENAME_NOT_EXP = 'ECB FX Rates NE.csv'

class Intrastat(str):
    """
    Global variables for intrastat class.
    """
    URL_EXP = 'https://github.com/homodudu/Data-Engineering/raw/main/intrastat/Intrastat%20Dispatches%20Data%20Sample.xlsx'
    INT_COLUMNS_DROP = ['Description_x', 'Mass (grams)', 'Shipping Date', 'Ship From', 'Incoterms', 'Transaction','CN8','SU',
                        'Description_y', 'CC Check', 'Net (EUR)', 'EUR to SEK']
    INT_COLUMNS_EXP = ['Ship To', 'Commodity Code','Net (SEK)', 'Quantity', 'Mass (KG)', 'County of Origin', 'Mode of Transport', 'Partner VAT' ]
    OUTPUT_FILENAME = 'Intrastat Submission Sample.xlsx'
