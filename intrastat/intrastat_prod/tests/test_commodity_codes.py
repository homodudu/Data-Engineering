"""
Testing of the CommodityCodes class.
"""
import unittest
import urllib.error as er
import intra.commodity_codes as cc
import intra.constants as cn
import pandas as pd

class TestCommodityCodes(unittest.TestCase):
    """
    Unittest the CommodityCodes component methods.
    """
    def setUp(self):
        """
        Set up the test environment.

        url_exp: The expected url to test.
        url_not_exp: The unexpected url to test.
        data_columns_test_exp: The expected dataframe columns to test.
        data_columns_test_not_exp: The not expected dataframe columns to test.
        data_body_test_exp: The expected dataframe body test.
        data_body_test_not_exp: The not expected dataframe body test.
        data_test_exp: The expected fx data sample to test.
        data_test_not_exp: The not expected fx data sample to test.
        digit_len_exp: The expected commodity code string length to test.
        filename_exp: The expected output filename to test.
        filename_not_exp: The not expected output filename to test.
        """
        # Define the class arguments
        self.url_exp = str(cn.CommodityCodes.URL_EXP)
        self.url_not_exp = str(cn.CommodityCodes.URL_NOT_EXP)
        self.cols_exp = cn.CommodityCodes.COLUMNS_EXP
        self.cols_not_exp = cn.CommodityCodes.COLUMNS_NOT_EXP
        self.body_exp = cn.CommodityCodes.BODY_EXP
        self.body_not_exp = cn.CommodityCodes.BODY_NOT_EXP
        self.str_len_exp = cn.CommodityCodes.STR_LEN_EXP
        self.filename_exp = cn.CommodityCodes.FILENAME_EXP
        self.filename_not_exp = cn.CommodityCodes.FILENAME_NOT_EXP

    def test_read_ok(self):
        """
        Test if commodity code url content has been read into dataframe as exepected.
        """
        # Method execution
        df_result = cc.CommodityCodesRTE().read(self.url_exp)
        # Test after method execution
        self.assertFalse(df_result.empty)

    def test_read_fail_bad_url(self):
        """
        Test if commodity code url content has not been read into the dataframe due to unexpected url.
        """
        # Method execution
        with self.assertRaises(er.HTTPError) as context:
            cc.CommodityCodesRTE().read(self.url_not_exp)
        # Test after method execution
        self.assertEqual(context.exception.code, 404)

    def test_transform_ok(self):
        """
        Test if commodity code dataframe has been transformed as expected.
        """
        # Test init
        df = pd.DataFrame(self.body_exp, columns=self.cols_exp)
        # Expected results
        col_exp = 'CN8'
        # Method execution
        df_res = cc.CommodityCodesRTE().transform(df)
        # Test after method execution
        self.assertEqual(len(df_res.iloc[0,0]), self.str_len_exp)
        col_res = df_res.columns.values[0]
        self.assertEqual(col_res, col_exp)

    def test_transform_fail_bad_data(self):
        """
        Test if commodity code dataframe has not been transformed due to unexpected data.
        """
        # Test init
        df = pd.DataFrame(self.body_not_exp, columns=self.cols_not_exp)
        # Method execution
        df_res = cc.CommodityCodesRTE().transform(df)
        # Test after method execution
        self.assertNotEqual(len(df_res.iloc[0,0]), self.str_len_exp)

    def test_export_ok(self):
        """
        Test if commodity code dataframe has exported as expected.
        """
        # Define test arguments
        df = pd.DataFrame(self.body_exp, columns=self.cols_exp)
        # Method execution
        cc.CommodityCodesRTE().export(df)
        # Test after method execution
        df_res = pd.read_csv(self.filename_exp, dtype=str)
        self.assertTrue(df_res.equals(df))
        print(df)
        print(df_res)

    def test_export_fail_missing_file(self):
        """
        Test if commodity code dataframe has not been exported if file not found for reading.
        """
        # Test init
        df = pd.DataFrame(self.body_exp, columns=self.cols_exp)
        # Method execution
        cc.CommodityCodesRTE().export(df)
        # Test after method execution
        with self.assertRaises(FileNotFoundError):
            pd.read_csv(self.filename_not_exp, dtype=str)

    def test_rte_process_ok(self):
        """
        Test if rte process has run as expected.
        """
        # Method execution
        df_res = cc.CommodityCodesRTE().rte_process(self.url_exp)
        # Test after method execution
        self.assertFalse(df_res.empty)

    def test_rte_process_fail_bad_url(self):
        """
        Test if rte process has failed due to unexpected url.
        """
        # Method execution with test
        with self.assertRaises(er.HTTPError):
            cc.CommodityCodesRTE().rte_process(self.url_not_exp)

    def tearDown(self):
        """
        Execute after unit tests.
        """

if __name__ == '__main__':
    unittest.main()
