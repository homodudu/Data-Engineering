"""
Testing of the FxRates class.
"""
import unittest
import intra.fx_rates as fx
import intra.constants as cn
import pandas as pd

class TestFxRates(unittest.TestCase):
    """
    Unittest the FxRates methods.
    """
    def setUp(self):
        """
        Set up the test environment.

        xml_object_test_exp: The data populated xml object to test.
        xml_object_test_not_exp: The blank xml object to test.
        xml_namespaces: The xml namespace test parameter.
        xml_child: The xml child test parameter.
        url_exp: The expected url to test.
        url_not_exp: The unexpected url to test.
        fx_data_columns_test_exp: The expected dataframe columns to test.
        fx_data_columns_test_not_exp: The unexpected dataframe columns to test.
        fx_data_body_test_exp: The expected fx data sample to test.
        """
        # Define the class arguments
        self.xml_obj_exp = cn.FxRates.XML_OBJECT_EXP
        self.xml_obj_not_exp = cn.FxRates.XML_OBJECT_NOT_EXP
        self.n_space_exp = cn.FxRates.XML_NAMESPACES_EXP
        self.n_space_not_exp = cn.FxRates.XML_NAMESPACES_NOT_EXP
        self.child_exp = cn.FxRates.XML_CHILD_EXP
        self.child_not_exp = cn.FxRates.XML_CHILD_NOT_EXP
        self.url_exp = cn.FxRates.URL_EXP
        self.url_not_exp = cn.FxRates.URL_NOT_EXP
        self.cols_exp = cn.FxRates.COLUMNS_EXP
        self.cols_not_exp = cn.FxRates.COLUMNS_NOT_EXP
        self.body_exp = cn.FxRates.BODY_EXP
        self.filename_exp = cn.FxRates.FILENAME_EXP
        self.filename_not_exp = cn.FxRates.FILENAME_NOT_EXP

    def test_read_ok(self):
        """
        Test if the xml resource has been read as expected.
        """
        # Method execution
        df_res = fx.FxRatesRTE().read(self.url_exp, self.child_exp, self.n_space_exp)
        # Test after method execution
        cols_res =  [c for c in df_res]
        self.assertEqual(cols_res, self.cols_exp)
        self.assertFalse(df_res.empty)

    def test_read_fail_bad_url(self):
        """
        Test if the fx resource has not been read due to unexpected url.
        """
        # Method execution
        with self.assertRaises(UnboundLocalError):
            df_res = fx.FxRatesRTE().read(self.url_not_exp, self.child_exp, self.n_space_exp)
            # Test after method execution
            self.assertTrue(df_res.empty)

    def test_read_empty_bad_child(self):
        """
        Test if the fx resource returns empty dataframe due to unexpected child element.
        """
        df_res = fx.FxRatesRTE().read(self.url_exp, self.child_not_exp, self.n_space_exp)
        self.assertTrue(df_res.empty)

    def test_read_empty_bad_namespace(self):
        """
        Test if the fx resource returns empty dataframe due to unexpected xml namespace.
        """
        df_res = fx.FxRatesRTE().read(self.url_exp, self.child_exp, self.n_space_not_exp)
        self.assertTrue(df_res.empty)

    def test_transform_ok(self):
        """
        Test if the fx dataframe has been transformed as expected.
        """
        # Test init
        df = pd.DataFrame(self.body_exp, columns=self.cols_exp)
        # Expected results
        df_exp = pd.DataFrame()
        df_exp.index = pd.date_range(self.body_exp[0][0], self.body_exp[-1][0])
        df_exp['EUR'] = 1.0
        df_exp = df_exp.sort_index(ascending=False)
        # Method execution
        df_res = fx.FxRatesRTE().transform(df)
        # Test after method execution
        self.assertTrue(df_res.equals(df_exp))

    def test_transform_fail_bad_data(self):
        """
        Test if the fx dataframee has not been transformed due to unexpected input data.
        """
        # Test init
        df = pd.DataFrame()
        # Method execution with test
        with self.assertRaises(KeyError):
            fx.FxRatesRTE().transform(df)

    def test_export_ok(self):
        """
        Test if fx dataframe has exported as expected.
        """
        # Test Init
        df = pd.DataFrame(self.body_exp, columns=self.cols_exp)
        # Method execution
        fx.FxRatesRTE().export(df)
        # Test after method execution
        df_res = pd.read_csv(self.filename_exp, dtype=str, index_col=0)
        df_res.columns.values[0] = 'Date'
        self.assertTrue(df_res.equals(df))

    def test_export_fail_missing_file(self):
        """
        Test if commodity code dataframe has not been exported if file not found for reading.
        """
        # Test init
        df = pd.DataFrame(self.body_exp, columns=self.cols_exp)
        # Method execution
        fx.FxRatesRTE().export(df)
        # Test after method execution
        with self.assertRaises(FileNotFoundError):
            pd.read_csv(self.filename_not_exp, dtype=str)

    def test_rte_process_ok(self):
        """
        Test if rte process has run as expected.
        """
        # Method execution
        df_res = fx.FxRatesRTE().rte_process(self.url_exp, self.child_exp, self.n_space_exp)
        # Test after method execution
        self.assertFalse(df_res.empty)

    def test_rte_process_fail_bad_url(self):
        """
        Test if rte process has failed due to unexpected url.
        """
        # Method execution with test
        with self.assertRaises(ValueError):
            fx.FxRatesRTE().rte_process(self.url_exp, self.child_not_exp, self.n_space_exp)

    def test_rte_process_fail_bad_child(self):
        """
        Test if rte process has failed due to unexpected child element.
        """
        # Method execution with test
        with self.assertRaises(UnboundLocalError):
            fx.FxRatesRTE().rte_process(self.url_not_exp, self.child_not_exp, self.n_space_exp)

    def test_rte_process_fail_bad_namespace(self):
        """
        Test if rte process has failed due to unexpected xml namespace.
        """
        # Method execution with test
        with self.assertRaises(ValueError):
            fx.FxRatesRTE().rte_process(self.url_exp, self.child_exp, self.n_space_not_exp)

    def tearDown(self):
        """
        Execute after unit tests.
        """

if __name__ == '__main__':
    unittest.main()
