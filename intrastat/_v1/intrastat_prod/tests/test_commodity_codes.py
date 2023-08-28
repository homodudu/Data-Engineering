"""
Testing of the CommodityCodes class.
"""
import unittest
import urllib.error as er
import intra.commodity_codes as cc
import intra.constants as cn
import pandas as pd

class TestCommodityCodesInteg(unittest.TestCase):
    """
    Integration testing of the CommodityCodes class.
    """
    def setUp(self):
        """
        Set up the test environment.

        url_exp: The expected commodity code url to test.
        url_not_exp: The unexpected commodity code url to test.
        cols_exp: The expected commodity code dataframe columns to test.
        cols_not_exp: The unexpected commodity code dataframe columns to test.
        body_exp: The expected commodity code dataframe body test.
        body_not_exp: The unexpected commodity code dataframe body test.
        str_len_exp: The expected commodity code string length to test.
        out_filename_exp: The expected output filename to test.
        out_filename_not_exp: The not expected output filename to test.
        """
        # Define the class arguments
        self.url_exp = str(cn.CommodityCodes.URL)
        self.url_not_exp = str(cn.CommodityCodes.URL_NOT_EXP)
        self.cols_exp = cn.CommodityCodes.COLUMNS_EXP
        self.cols_not_exp = cn.CommodityCodes.COLUMNS_NOT_EXP
        self.body_exp = cn.CommodityCodes.BODY_EXP
        self.body_not_exp = cn.CommodityCodes.BODY_NOT_EXP
        self.str_len_exp = cn.CommodityCodes.STR_LEN_EXP
        self.out_filename_exp = cn.CommodityCodes.OUTPUT_FILENAME
        self.out_filename_not_exp = cn.CommodityCodes.OUTPUT_FILENAME_NOT_EXP

    def test_read_ok(self):
        """
        Test if cc url content has been read as exepected.
        """
        # Method execution
        df_result = cc.CommodityCodesRTE().read(self.url_exp)
        # Test after method execution
        self.assertFalse(df_result.empty)

    def test_read_fail_unknown_url(self):
        """
        Test if cc url content has not been read due to unexpected url.
        """
        # Method execution
        with self.assertRaises(er.HTTPError) as context:
            cc.CommodityCodesRTE().read(self.url_not_exp)
        # Test after method execution
        self.assertEqual(context.exception.code, 404)

    def test_transform_ok(self):
        """
        Test if cc dataframe has been transformed as expected.
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

    def test_transform_fail_incorrect_cc_length(self):
        """
        Test if cc dataframe has not been transformed due to incorrect cc string length.
        """
        # Test init
        df = pd.DataFrame(self.body_not_exp, columns=self.cols_not_exp)
        # Method execution
        df_res = cc.CommodityCodesRTE().transform(df)
        # Test after method execution
        self.assertNotEqual(len(df_res.iloc[0,0]), self.str_len_exp)

    def test_export_ok(self):
        """
        Test if cc dataframe has exported as expected.
        """
        # Define test arguments
        df = pd.DataFrame(self.body_exp, columns=self.cols_exp)
        # Method execution
        cc.CommodityCodesRTE().export(df)
        # Test after method execution
        df_res = pd.read_csv(self.out_filename_exp, dtype=str)
        self.assertTrue(df_res.equals(df))

    def test_export_fail_missing_file(self):
        """
        Test if cc dataframe has not been exported if file not found for reading.
        """
        # Test init
        df = pd.DataFrame(self.body_exp, columns=self.cols_exp)
        # Method execution
        cc.CommodityCodesRTE().export(df)
        # Test after method execution
        with self.assertRaises(FileNotFoundError):
            pd.read_csv(self.out_filename_not_exp, dtype=str)

    def test_rte_process_ok(self):
        """
        Test if rte process has run as expected.
        """
        # Method execution
        df_res = cc.CommodityCodesRTE().rte_process(self.url_exp)
        # Test after method execution
        self.assertFalse(df_res.empty)

    def test_rte_process_fail_unkown_url(self):
        """
        Test if rte process has failed due to unexpected url.
        """
        # Method execution
        with self.assertRaises(er.HTTPError) as context:
            cc.CommodityCodesRTE().rte_process(self.url_not_exp)
        # Test after method execution
        self.assertEqual(context.exception.code, 404)

    def tearDown(self):
        """
        Execute after unit tests.
        """

if __name__ == '__main__':
    unittest.main()
