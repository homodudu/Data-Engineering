"""
Test CommodityCodes Component.
"""
import unittest
import urllib.error as er
import intra.commodity_codes as cc
import intra.constants as cn

class TestCommodityCodes(unittest.TestCase):
    """
    Integration testing of the CommodityCodes class.
    """
    def setUp(self):
        """
        Set up the test environment.

        :url_correct - the correct url to test
        :url_incorrect: the incorrect url to test
        """
        self.url_exp = str(cn.CommodityCodes.URL_EXP)
        self.url_not_exp = str(cn.CommodityCodes.URL_NOT_EXP)

    def test_read_cc_to_dataframe_ok(self):
        """
        Test if commodity code url content has been read into dataframe.
        """
        # Method execution
        df_result = cc.CommodityCodes().read(self.url_exp)
        # Test after method execution
        self.assertFalse(df_result.empty)

    def test_read_cc_to_dataframe_fail(self):
        """
        Test if commodity code url content has not been read into the dataframe.
        """
        # Method execution with test
        with self.assertRaises(er.HTTPError):
            cc.CommodityCodes().read(self.url_not_exp)

    def tearDown(self):
        """
        Execute after unit tests.
        """

if __name__ == '__main__':
    unittest.main()
