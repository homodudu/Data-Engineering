"""
Test CommodityCodes Component.
"""
import unittest
import datetime as dt
import intra.fx_rates as fx
import intra.constants as cn
import pandas as pd


class TestFxRates(unittest.TestCase):
    """
    Integration testing of the CommodityCodes class.
    """
    def setUp(self):
        """
        Set up the test environment.

        :xml_namespaces - the xml namepsace test parameter
        :xml_child - the xml child test parameter
        :url_correct - the correct url to test
        :url_incorrect: the incorrect url to test
        """

        # Disable security certificate checks for url requests.
        self.xml_object_test_ok = cn.FxRates.XML_OBJECT_TEST_OK
        self.xml_object_test_fail = cn.FxRates.XML_OBJECT_TEST_FAIL
        self.xml_namespaces = cn.FxRates.XML_NAMESPACES
        self.xml_child = cn.FxRates.XML_CHILD
        self.url_correct = cn.FxRates.URL_USE
        self.url_incorrect = cn.FxRates.URL_TEST
        self.xml_parse_columns_exp = cn.FxRates.XML_PARSE_COLUMNS_EXP
        self.fx_data_test = cn.FxRates.FX_DATA_TEST_OK

    def test_parse_xml_ok(self):
        """
        Test if fx rate xml content has been parsed and read into a data frame.
        """
        # Method execution
        df_res = fx.FxRates().parse_xml(self.xml_object_test_ok, self.xml_child, self.xml_namespaces)
        # Test after method execution
        columns_res = [c for c in df_res]
        self.assertEqual(columns_res, self.xml_parse_columns_exp)
        self.assertFalse(df_res.empty)

    def test_parse_xml_fail(self):
        """
        Test if fx rate xml content has not been parsed and read into a data frame.
        """
        # Method execution
        df_res = fx.FxRates().parse_xml(self.xml_object_test_fail, self.xml_child, self.xml_namespaces)
        # Test after method execution
        self.assertTrue(df_res.empty)

    def test_create_pivot_dates(self):
        """
        Test if dataframe returned by by create_pivot() has been reindexed to include weekend dates.
        """
        data = [['2022-12-30','EUR','1.00'],['2023-01-06','EUR','1.00']]
        df = pd.DataFrame(data, columns=self.xml_parse_columns_exp)
        # Expected results
        df_exp = pd.DataFrame(self.fx_data_test, columns=self.xml_parse_columns_exp)
        dates_exp = [d for d in df_exp['Date']]
        # Method execution
        df_res = fx.FxRates().create_pivot(df)
        dates_res = [str(dt.datetime.strftime(d, '%Y-%m-%d')) for d in df_res.index][::-1]
        print(dates_exp)
        print(dates_res)
        # Test after method execution
        self.assertEqual(dates_res, dates_exp)

    def tearDown(self):
        """
        Execute after unit tests.
        """

if __name__ == '__main__':
    unittest.main()
