"""
Intrastat data processing component.
"""
import ssl # Secure sockets layer package.
import urllib.request # Url request handling module.
import pandas as pd # Data analysis library.
import numpy as np # Array and matrice libary.
import intra.constants as cn

class IntrastatRATE():
    """
    Read, analyse, transform and export intrastat data.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for Intrastat class.
        """
        # Disable security certificate checks for url requests.
        ssl._create_default_https_context = ssl._create_unverified_context
        self.url = cn.Intrastat.URL_EXP
        self.int_columns_drop = cn.Intrastat.INT_COLUMNS_DROP
        self.int_columns_exp = cn.Intrastat.INT_COLUMNS_EXP

    def return_mot(self, mode: str):
        """
        Return mode of transport code from string.

        mode: The mode of transport.
        """
        mot_switch={'Sea':'1', 'Rail':'2','Road':'3', 'Air':'4'}
        return mot_switch.get(mode,"Invalid mode of transport\n")

    def cc_check(self, df_src: pd.DataFrame, df_cc: pd.DataFrame):
        """
        Check source commodity codes match the official codes.

        df_src: Dataframe containing the source commodity codes.
        df_cc: Dataframe containing the official commodity codes.
        """
        df_src['Commodity Code'] = df_src['Commodity Code'].astype(str)
        df_out = pd.merge(df_src, df_cc, how='left', left_on='Commodity Code', right_on='CN8')
        df_out['CC Check'] = np.where(df_out['Commodity Code'] == df_out['CN8'], 'OK', '`ERROR')
        return df_out

    def fx_convert(self, df_src: pd.DataFrame, df_fx: pd.DataFrame):
        """
        Perform fx rate conversion on source data invoices by shipping date reference.

        df_src: Dataframe containing the source file invoice values.
        df_fx: Dataframe containing the foreign exchange values.
        """
        df_src['Shipping Date'] = df_src['Shipping Date'].astype("string")
        df_src['Shipping Date'] = pd.to_datetime(df_src['Shipping Date'], format="%d-%m-%Y")
        df_out = pd.merge(df_src, df_fx, how='left', left_on='Shipping Date', right_on=df_fx.index)
        df_out.rename(columns = {'SEK':'EUR to SEK'}, inplace = True)
        df_out['Net (SEK)'] = df_out['Net (EUR)'].astype('float').multiply(df_out['EUR to SEK'].astype('float'))
        return df_out

    def read(self, url: str):
        """
        Read the intrastat source data into a dataframe.

        url: The url of the intrastat source data to read.
        """
        # Read data into pandas dataframe.
        with urllib.request.urlopen(url) as src_url:
            try:
                df = pd.read_excel(src_url.read())
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print('Error: Requested source data url is invalid.')
        return df

    def analyse(self, df_src: pd.DataFrame, df_cc: pd.DataFrame, df_fx: pd.DataFrame):
        """
        Analyse source data through commodity code checks and fx rate conversions.

        df_src: Dataframe containing the source data to analyse.
        df_cc: Dataframe containing the official commodity codes.
        df_fx: Dataframe containing the foreign exchange values.
        """
        df_cc_check = self.cc_check(df_src, df_cc)
        df_fx_convert = self.fx_convert(df_cc_check, df_fx)
        return df_fx_convert

    def transform(self, df_src: pd.DataFrame):
        """
        Transform the column data (intrastat fields)i into format for intrastat submission.

        df_src: Dataframe containing the source data to transform.
        """
        df_src['Mode of Transport'] = [self.return_mot(mode) for mode in df_src['Mode of Transport']]
        df_src['Partner VAT'] = np.where(df_src['Transaction'] == 'B2C', 'QV999999999999', df_src['Partner VAT'])
        df_src['Mass (KG)'] = df_src['Mass (grams)'].astype('float').multiply(0.001)
        df_src["County of Origin"] = 'CN'
        df_src = df_src.drop(self.int_columns_drop, axis = 1)
        df_src = df_src[self.int_columns_exp]
        return df_src

    def export(self, file_name: str, df: pd.DataFrame):
        """
        Export the transformed data to an excel output file.

        filename: The file name of the output data.
        df: Dataframe containing the source data to export.
        """
        df.iloc[:,0] = df.iloc[:,0].astype("str")
        df.to_excel(file_name, index=False)
        print('\nMessage: Submission file successfully exported.')
        print('4. Intrastat Submission File')
        print(df)

    def rate_process(self, url: str, df_cc: pd.DataFrame, df_fx: pd.DataFrame, file_name: str):
        """
        url: The url of the intrastat input data.
        df_cc: Dataframe containing the official commodity codes.
        df_fx: Dataframe containing the foreign exchange values.
        filename: The file name of the intrastat output data.
        """
        # Perform full read, analyse, transform and export process.
        df_read = self.read(url)
        df_analyse = self.analyse(df_read, df_cc, df_fx)
        df_transform = self.transform(df_analyse)
        self.export(file_name, df_transform)
