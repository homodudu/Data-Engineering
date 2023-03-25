"""
File to store constants
"""
class CommodityCodes(str):
    """
    Constants for commodity codes and test class.
    """
    # Global Arguments
    URL = 'https://www.cbs.nl/-/media/cbsvooruwbedrijf/international-trade-in-goods/commoditycodes-2023.xlsx'
    OUTPUT_FILENAME = 'CN8 Codes.csv'
    # Test Arguments
    URL_NOT_EXP = 'https://www.cbs.nl/-/media/cbsvooruwbedrijf/international-trade-in-goods/commoditycodes-XXXX.xlsx'
    COLUMNS_EXP= ['Commodity Code','SU', 'Description']
    COLUMNS_NOT_EXP = ['X','Y', 'Z']
    BODY_EXP = [['61012010','p/st','CC Description']]
    BODY_NOT_EXP = [['610120100','p/st','CC Description']]
    STR_LEN_EXP = 8
    SU_EXP = 'p/st'
    OUTPUT_FILENAME_NOT_EXP = 'CN8 Codes NE.csv'

class FxRates(str):
    """
    Constants for fx rates and test class.
    """
    # Global Arguments
    URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml'
    XML_NAMESPACES = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    XML_CHILD = './/ex:Cube'
    OUTPUT_FILENAME = 'ECB FX Rates.csv'
    # Test Arguments
    URL_NOT_EXP = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-XXd.xml'
    XML_NAMESPACES_NOT_EXP = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofXXXX'}
    XML_CHILD_NOT_EXP = './/ex:XXXX'
    XML_OBJECT_EXP = '_resources/eurofxref-hist-90d_test_exp.xml'
    XML_OBJECT_NOT_EXP = '_resources/eurofxref-hist-90d_test_not_exp.xml'
    COLUMNS_EXP= ['Date','Currency', 'Rate']
    COLUMNS_NOT_EXP = ['X','Y', 'Z']
    FX_EXP = '10.00'
    NET_EXP = 1900.0
    BODY_EXP = [['2022-12-30','EUR','1.00'],
                ['2022-12-31','EUR','1.00'],
                ['2023-01-01','EUR','1.00'],
                ['2023-01-02','EUR','1.00'],
                ['2023-01-03','EUR','1.00'],
                ['2023-01-04','EUR','1.00'],
                ['2023-01-05','EUR','1.00'],
                ['2023-01-06','EUR','1.00'],
                ['2023-01-07','EUR','1.00']]
    FX_PIVOT_COLUMNS_EXP = ['Date','SEK']
    FX_PIVOT_BODY_EXP = [['2022-12-30','10.00'],
                        ['2022-12-31','10.00'],
                        ['2023-01-01','10.00'],
                        ['2023-01-02','10.00'],
                        ['2023-01-03','10.00'],
                        ['2023-01-04','10.00'],
                        ['2023-01-05','10.00'],
                        ['2023-01-06','10.00'],
                        ['2023-01-07','10.00']]
    OUTPUT_FILENAME_NOT_EXP = 'ECB FX Rates NE.csv'

class Intrastat(str):
    """
    Constants for intrastat and test class.
    """
    # Global Arguments
    URL = 'https://github.com/homodudu/Data-Engineering/raw/main/intrastat/_resources/Intrastat%20Data%20Sample.xlsx'
    COLUMNS_DROP = ['Description_x', 'Mass (grams)', 'Shipping Date', 'Ship From', 'Incoterms', 'Transaction','CN8','SU',
                        'Description_y', 'CC Check', 'Net (EUR)', 'EUR to SEK']
    OUTPUT_FILENAME = 'Intrastat Submission Sample.xlsx'
    RETURN_MOT = {'Sea':'1', 'Rail':'2','Road':'3', 'Air':'4'}
    # Test Arguments
    URL_NOT_EXP = 'https://github.com/homodudu/Data-Engineering/raw/main/intrastat/Intrastat%20Dispatches%20DataXXXXXXXX.xlsx'
    COLUMNS_EXP = ['Ship To', 'Commodity Code','Net (SEK)', 'Quantity', 'Mass (KG)', 'County of Origin', 'Mode of Transport', 'Partner VAT' ]
    MOT_EXP = 'Road'
    MOT_NOT_EXP = 'Spaceship'
    RET_MOT_CODE_EXP = '3'
    INPUT_FILENAME_EXP = '_resources/intrastat_data_sample_exp.xlsx'
    INPUT_FILENAME_NOT_EXP = '_resources/intrastat_data_sample_not_exp.xlsx'
    OUTPUT_FILENAME_NOT_EXP = 'Intrastat Submission Sample NE.xlsx'
    READ_COLUMNS_EXP = ['Commodity Code', 'Description', 'Mass (grams)', 'Net (EUR)', 'Quantity', 'Shipping Date',
                        'Ship From','Ship To', 'County of Origin', 'Mode of Transport', 'Incoterms', 'Transaction',
                        'Partner VAT']
    READ_BODY_EXP = ['61012010', "Men's or boys' overcoats", '595','190', '1', '2023-04-01', 'SE', 'DE', 'China', 'Rail', 'DAP',
                        'B2C', 'Private Customer']
    ANALY_COLUMNS_EXP = ['Commodity Code', 'Description_x', 'Mass (grams)', 'Net (EUR)', 'Quantity', 'Shipping Date',
                        'Ship From','Ship To', 'County of Origin', 'Mode of Transport', 'Incoterms', 'Transaction',
                        'Partner VAT', 'CN8', 'SU', 'Description_y', 'CC Check', 'EUR to SEK', 'Net (SEK)']
    ANALY_BODY_EXP = ['61012010', "Men's or boys' overcoats", '595','190', '1', '2023-01-04', 'SE', 'DE', 'China', 'Rail', 'DAP',
                        'B2C', 'Private Customer', '61012010',  'p/st', 'CC Description', 'OK', '10.00', '1900.0']
    TRANS_BODY_EXP = ['DE', '61012010', '1900.0','1','0.595', 'CN', '2', 'QV999999999999']
