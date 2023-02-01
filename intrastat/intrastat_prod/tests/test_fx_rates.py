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

        xml_object_test_ok: The data populated xml object to test.
        xml_object_test_fail: The blank xml object to test.
        xml_namespaces: The xml namespace test parameter.
        xml_child: The xml child test parameter.
        url_correct: The correct url to test.
        url_incorrect: The incorrect url to test.
        xml_columns_ok: The expected dataframe columns to test.
        xml_columns_fail: The unexpected dataframe columns to test.
        fx_data_test_exp: The expected fx data sample to test.
        """
        self.xml_object_test_exp = cn.FxRates.XML_OBJECT_TEST_EXP
        self.xml_object_test_not_exp = cn.FxRates.XML_OBJECT_TEST_NOT_EXP
        self.xml_namespaces = cn.FxRates.XML_NAMESPACES
        self.xml_child = cn.FxRates.XML_CHILD
        self.url_exp = cn.FxRates.URL_EXP
        self.url_not_exp = cn.FxRates.URL_NOT_EXP
        self.fx_data_columns_test_exp = cn.FxRates.FX_DATA_COLUMNS_TEST_EXP
        self.fx_data_columns_test_not_exp = cn.FxRates.FX_DATA_COLUMNS_TEST_NOT_EXP
        self.fx_data_body_test_exp = cn.FxRates.FX_DATA_BODY_TEST_EXP

    def test_parse_xml_ok(self):
        """
        Test if fx rate xml content has been parsed and read into a data frame.
        """
        # Method execution
        df_res = fx.FxRates().parse_xml(self.xml_object_test_exp, self.xml_child, self.xml_namespaces)
        # Test after method execution
        columns_res = [c for c in df_res]
        self.assertEqual(columns_res, self.fx_data_columns_test_exp)
        self.assertFalse(df_res.empty)

    def test_parse_xml_fail(self):
        """
        Test if fx rate xml content has not been parsed and read into a data frame.
        """
        # Method execution
        df_res = fx.FxRates().parse_xml(self.xml_object_test_not_exp, self.xml_child, self.xml_namespaces)
        # Test after method execution
        self.assertTrue(df_res.empty)

    def test_create_pivot_dates_ok(self):
        """
        Test if dataframe returned by create_pivot() has been reindexed to include weekend dates.
        """
        # Create test input dataframe
        data = self.fx_data_body_test_exp
        df = pd.DataFrame(data, columns=self.fx_data_columns_test_exp)
        # Expected results
        dates_exp = [d[0] for d in self.fx_data_body_test_exp]
        # Method execution
        df_res = fx.FxRates().create_pivot(df)
        dates_res = [str(dt.datetime.strftime(d, '%Y-%m-%d')) for d in df_res.index][::-1]
        # Test after method execution
        self.assertEqual(dates_res, dates_exp)

    def test_create_pivot_dataframe_ok(self):
        """
        Test if dataframe passed into create_pivot() is expected format and returns expected data.
        """
        # Create test input dataframe
        data = self.fx_data_body_test_exp
        df = pd.DataFrame(data, columns=self.fx_data_columns_test_exp)
        # Expected results
        df_exp = pd.DataFrame()
        df_exp.index = pd.date_range(data[0][0], data[-1][0])
        df_exp['EUR'] = 1.0
        df_exp = df_exp.sort_index(ascending=False)
        # Method execution
        df_res = fx.FxRates().create_pivot(df)
        # Test after method execution
        self.assertTrue(df_res.equals(df_exp))

    def test_create_pivot_dataframe_fail(self):
        """
        Test if dataframe passed into create_pivot() contains unexpected columns
        """
        # Create test input dataframe
        data = self.fx_data_body_test_exp
        df = pd.DataFrame(data, columns=self.fx_data_columns_test_not_exp)
        # Method execution with test
        with self.assertRaises(KeyError):
            fx.FxRates().create_pivot(df)

    def test_create_pivot_dataframe_empty(self):
        """
        Test if dataframe returned by create_pivot() is empty
        """
        # Create test input dataframe
        df = pd.DataFrame()
        # Method execution with test
        with self.assertRaises(KeyError):
            fx.FxRates().create_pivot(df)

    def tearDown(self):
        """
        Execute after unit tests.
        """

if __name__ == '__main__':
    unittest.main()
