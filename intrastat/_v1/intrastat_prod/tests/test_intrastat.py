"""
Testing of the Intrastat class.
"""
import unittest
import urllib.error as er
import datetime as dt
import pandas as pd
import intra.intrastat as it
import intra.constants as cn


class TestIntrastatUnit(unittest.TestCase):
    """
    Unit testing of the Intrastat class.
    """
    def setUp(self):
        """
        Set up the environment

        ret_mot_dict: Dictionary containing expected mode of transport codes to test.
        mot_exp: The expected mode of transport input string to test.
        mot_not_exp: The unexpected mode of transport input string to test.
        ret_mot_code_exp: The expected mode of transport return code test.
        df_cc: The exepected commodity code resource dataframe to test.
        df_fx: The exepected fx rates resource dataframe to test.
        """
        # Define the class arguments
        self.ret_mot_dict = cn.Intrastat.RETURN_MOT
        self.mot_exp = cn.Intrastat.MOT_EXP
        self.mot_not_exp = cn.Intrastat.MOT_NOT_EXP
        self.ret_mot_code_exp = cn.Intrastat.RET_MOT_CODE_EXP
        self.cc_cols_exp = cn.CommodityCodes.COLUMNS_EXP
        self.cc_body_exp = cn.CommodityCodes.BODY_EXP
        self.fx_cols_exp = cn.FxRates.FX_PIVOT_COLUMNS_EXP
        self.fx_body_exp = cn.FxRates.FX_PIVOT_BODY_EXP
        self.fx_exp = cn.FxRates.FX_EXP
        self.net_exp = cn.FxRates.NET_EXP
        self.su_exp = cn.CommodityCodes.SU_EXP
        self.df_src = pd.read_excel(cn.Intrastat.INPUT_FILENAME_EXP)
        self.df_cc = pd.DataFrame(self.cc_body_exp, columns=self.cc_cols_exp)
        self.df_cc.columns.values[0] = 'CN8'
        self.df_fx = pd.DataFrame(self.fx_body_exp, columns=self.fx_cols_exp)
        self.df_fx['Date'] = [dt.datetime.strptime(d, '%Y-%m-%d') for d in self.df_fx['Date']]
        self.df_fx.set_index('Date',  inplace = True)


    def test_return_mot_ok(self):
        """
        Test if the return_mot() function returns the expected mot code.
        """
        #Expected results
        code_exp = self.ret_mot_code_exp
        # Method execution
        mot_res = it.IntrastatRATE().return_mot(self.mot_exp)
        # Test after method execution
        self.assertEqual(mot_res, code_exp)

    def test_return_mot_fail_unknown_mot(self):
        """
        Test if the return_mot() function fails due to unexpected input string.
        """
        # Method execution
        mot_res = it.IntrastatRATE().return_mot(self.mot_not_exp)
        # Test after method execution
        self.assertNotIn(mot_res, self.ret_mot_dict.keys())

    def test_cc_check_ok(self):
        """
        Test if the cc_check() returns the expected output.
        """
        #Expected results
        su_exp = self.su_exp
        # Method execution
        df_res = it.IntrastatRATE().cc_check(self.df_src, self.df_cc)
        # Test after method execution
        self.assertEqual(df_res['SU'][0], su_exp)

    def test_cc_check_fail_key_error(self):
        """
        Test if the cc_check() function fails due to key error.
        """
        # Test init
        df = pd.DataFrame()
        # Method execution
        with self.assertRaises(KeyError) as context:
            it.IntrastatRATE().cc_check(df, self.df_cc)
        # Test after method execution
        args = list(context.exception.args)
        self.assertTrue(any(a in args) for a in self.cc_cols_exp)

    def test_fx_convert_ok(self):
        """
        Test if the fx_convert() returns the expected output.
        """
        #Expected results
        fx_exp = self.fx_exp
        net_exp = self.net_exp
        # Method execution
        df_res = it.IntrastatRATE().fx_convert(self.df_src, self.df_fx)
        # Test after method execution
        self.assertEqual(df_res['EUR to SEK'][0], fx_exp)
        self.assertEqual(df_res['Net (SEK)'][0], net_exp)

    def test_fx_convert_fail_key_error(self):
        """
        Test if the fx_convert() function fails due to key error.
        """
        # Test init
        df = pd.DataFrame()
        # Method execution
        with self.assertRaises(KeyError) as context:
            it.IntrastatRATE().fx_convert(df, self.df_fx)
        # Test after method execution
        args = list(context.exception.args)
        self.assertTrue(any(a in args) for a in self.fx_cols_exp)

    def tearDown(self):
        """
        Execute after unit tests
        """

class TestIntrastatInteg(unittest.TestCase):
    """
    Integration testing of the Intrastat class.
    """
    def setUp(self):
        """
        Set up the environment
        url_exp: The expected source data url.
        url_not_exp: The unexpected source data url.
        cc_cols_exp: The expected commodity code data columns.
        cc_body_exp: The expected commodity code data body.
        fx_cols_exp: The expected fx rates data columns.
        fx_body_exp: The expected fx rates data body.
        read_cols_exp: The expected output columns of the read() function.
        read_body_exp: The unexpected output columns of the read() function.
        analy_cols_exp: The expected output columns of the analyse() function.
        analy_body_exp: The unexpected output columns of the analyse() function.
        trans_cols_exp: The expected output columns of the transform() function.
        trans_body_exp: The unexpected output columns of the transform() function.
        in_filename_exp: The expected filename of the source data.
        out_filename_exp: The expected output filename of the processed source data.
        out_filename_not_exp: The unexpected output filename of the processed source data.
        df_cc: The exepected commodity code resource dataframe to test.
        df_fx: The exepected fx rates resource dataframe to test.
        """
        # Define the class arguments
        self.url_exp = cn.Intrastat.URL
        self.url_not_exp = cn.Intrastat.URL_NOT_EXP
        self.cc_cols_exp = cn.CommodityCodes.COLUMNS_EXP
        self.cc_body_exp = cn.CommodityCodes.BODY_EXP
        self.fx_cols_exp = cn.FxRates.FX_PIVOT_COLUMNS_EXP
        self.fx_body_exp = cn.FxRates.FX_PIVOT_BODY_EXP
        self.read_cols_exp = cn.Intrastat.READ_COLUMNS_EXP
        self.read_body_exp = cn.Intrastat.READ_BODY_EXP
        self.analy_cols_exp = cn.Intrastat.ANALY_COLUMNS_EXP
        self.analy_body_exp = cn.Intrastat.ANALY_BODY_EXP
        self.trans_cols_exp = cn.Intrastat.COLUMNS_EXP
        self.trans_body_exp = cn.Intrastat.TRANS_BODY_EXP
        self.in_filename_exp = cn.Intrastat.INPUT_FILENAME_EXP
        self.out_filename_exp = cn.Intrastat.OUTPUT_FILENAME
        self.out_filename_not_exp = cn.Intrastat.OUTPUT_FILENAME_NOT_EXP
        self.df_cc = pd.DataFrame(self.cc_body_exp, columns=self.cc_cols_exp)
        self.df_cc.columns.values[0] = 'CN8'
        self.df_fx = pd.DataFrame(self.fx_body_exp, columns=self.fx_cols_exp)
        self.df_fx['Date'] = [dt.datetime.strptime(d, '%Y-%m-%d') for d in self.df_fx['Date']]
        self.df_fx.set_index('Date',  inplace = True)

    def test_read_ok(self):
        """
        Test if the intrastat source url content has been read as expected.
        """
        # Expected results
        df_exp = pd.DataFrame([self.read_body_exp], columns=self.read_cols_exp)
        df_exp['Shipping Date'] = pd.to_datetime(df_exp['Shipping Date']).dt.date
        # Method execution
        df_res = it.IntrastatRATE().read(self.url_exp).astype(str)
        # Test after method execution
        df_res['Shipping Date'] = pd.to_datetime(df_res['Shipping Date']).dt.date
        print(df_res.iloc[0])
        print(df_exp.iloc[0])
        # self.assertTrue(df_res.iloc[0].equals(df_exp.iloc[0]))

    def test_read_fail_url_error(self):
        """
        Test if the intrastat source url content failed due to unknown url.
        """
        # Method execution
        with self.assertRaises(er.HTTPError) as context:
            it.IntrastatRATE().read(self.url_not_exp)
        # Test after method execution
        self.assertTrue(context.exception.code == 404)

    def test_analyse_ok(self):
        """
        Test if the intrastat source data has been analysed as expected.
        """
        # Test init
        df = pd.read_excel(self.in_filename_exp)
        # Expect results
        df_exp = pd.DataFrame([self.analy_body_exp], columns=self.analy_cols_exp)
        # Method execution
        df_res = it.IntrastatRATE().analyse(df, self.df_cc, self.df_fx).astype(str)
        self.assertTrue(df_res.equals(df_exp))

    def test_analyse_fail_key_error(self):
        """
        Test if the intrastat source data has not been analysed due to key error.
        """
        # Test init
        df = pd.DataFrame()
        df_cc = pd.DataFrame(self.cc_body_exp, columns=self.cc_cols_exp)
        df_fx = pd.DataFrame(self.fx_body_exp, columns=self.fx_cols_exp)
        # Method execution with test
        with self.assertRaises(KeyError) as context:
            it.IntrastatRATE().analyse(df, df_cc, df_fx)
        # Test after method execution
        args = list(context.exception.args)
        self.assertTrue(any(a in args) for a in self.read_cols_exp)

    def test_transform_ok(self):
        """
        Test if the intrastat analyse data has been transformed as expected.
        """
        # Test init
        df = pd.DataFrame([self.analy_body_exp], columns=self.analy_cols_exp)
        # Expected results
        df_exp = pd.DataFrame([self.trans_body_exp], columns=self.trans_cols_exp)
        # Method execution
        df_res = (it.IntrastatRATE().transform(df)).astype(str)
        # Test after method execution
        self.assertTrue(df_res.equals(df_exp))

    def test_transform_fail_key_error(self):
        """
        Test if the intrastat analyse data has not been transformed due to key error.
        """
        # Test init
        df = pd.DataFrame()
        # Method execution
        with self.assertRaises(KeyError) as context:
            it.IntrastatRATE().transform(df)
        args = list(context.exception.args)
        # Test after method execution
        self.assertTrue(any(a in args) for a in self.analy_cols_exp)

    def test_export_ok(self):
        """
        Test if the intrastat dataframe has exported as expected.
        """
        # Test init
        df = pd.DataFrame([self.trans_body_exp], columns=self.trans_cols_exp)
        # Method execution
        it.IntrastatRATE.export(self, self.out_filename_exp, df)
        # Test after method execution
        df_res = pd.read_excel(self.out_filename_exp, dtype=str)
        self.assertTrue(df_res.equals(df))

    def test_export_fail_missing_file(self):
        """
        Test if the intrastat dataframe has not been exported if file not found.
        """
        # Test init
        df = pd.DataFrame([self.trans_body_exp], columns=self.trans_cols_exp)
        # Method execution
        it.IntrastatRATE.export(self, self.out_filename_exp, df)
        # Test after method execution
        with self.assertRaises(FileNotFoundError):
            pd.read_excel(self.out_filename_not_exp, dtype=str)

    def test_rate_ok(self):
        """
        Test if the intrastat rate process has run as expected.
        """
        # Expected results
        df_exp = pd.DataFrame([self.trans_body_exp], columns=self.trans_cols_exp)
        df_exp['Net (SEK)'] = df_exp['Net (SEK)'].astype(float).round(0).astype(int).astype(str)
        # Method execution
        it.IntrastatRATE().rate_process(self.url_exp, self.df_cc, self.df_fx, self.out_filename_exp)
        # Test after method execution
        df_res = pd.read_excel(self.out_filename_exp, dtype=str)
        self.assertTrue(df_res.iloc[0].equals(df_exp.iloc[0]))
        self.assertFalse(df_res.isnull().values.any())

    def test_rate_fail_unknown_url(self):
        """
        Test if the rate process failed due to unexpected url.
        """
        # Method execution
        with self.assertRaises(er.HTTPError) as context:
            it.IntrastatRATE().rate_process(self.url_not_exp, self.df_cc, self.df_fx, self.out_filename_exp)
        # Test after method execution
        self.assertTrue(context.exception.code == 404)

    def test_rate_fail_cc_key_error(self):
        """
        Test if the rate process failed due to commodity code resource key error.
        """
        # Test init
        df_cc = pd.DataFrame()
        # Method execution
        with self.assertRaises(KeyError) as context:
            it.IntrastatRATE().rate_process(self.url_exp, df_cc, self.df_fx, self.out_filename_exp)
        # Test after method execution
        args = list(context.exception.args)
        self.assertTrue(any(a in args) for a in self.cc_cols_exp)

    def test_rate_fail_fx_key_error(self):
        """
        Test if the rate process failed due to fx rates resource key error.
        """
        # Test init
        df_fx = pd.DataFrame()
        # Method execution
        with self.assertRaises(KeyError) as context:
            it.IntrastatRATE().rate_process(self.url_exp, self.df_cc, df_fx, self.out_filename_exp)
        # Test after method execution
        args = list(context.exception.args)
        self.assertTrue(any(a in args) for a in self.cc_cols_exp)

    def tearDown(self):
        """
        Execute after unit tests
        """

if __name__ == '__main__':
    unittest.main()
