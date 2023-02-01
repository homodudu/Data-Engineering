"""
Intrastat data processing component.
"""

import urllib.request # Url request handling module.
import pandas as pd # Data analysis library.
import numpy as np # Array and matrice libary.
import intra.constants as cn
import intra.fx_rates as fx
import intra.commodity_codes as cc

class Intrastat():
    """
    Read, analyse, transform and export intrastat data.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for Intrastat class.
        """
        self.src_url = cn.Intrastat.URL_SRC_EXP

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
        df_out = pd.merge(df_src, df_cc, how='left', left_on='Commodity Code', right_on='CN8')
        df_out['CC Check'] = np.where(df_out['Commodity Code'] == df_out['CN8'], 'OK', '`ERROR')
        return df_out

    def src_fx_convert(self, df_src: pd.DataFrame, df_fx: pd.DataFrame):
        """
        Perform fx rate conversion on source data invoices by shipping date reference.

        df_src: Dataframe containing the source invoice values.
        df_fx: Dataframe containing the foreign exchange values.
        """
        df_src['Shipping Date'] = df_src['Shipping Date'].astype("string")
        df_src['Shipping Date'] = pd.to_datetime(df_src['Shipping Date'], format="%d-%m-%Y")
        df_out = pd.merge(df_src, df_fx, how='left', left_on='Shipping Date', right_on=df_fx.index)
        df_out.rename(columns = {'SEK':'EUR to SEK'}, inplace = True)
        df_out['Net (SEK)'] = df_out['Net (EUR)'].astype('float').multiply(df_out['EUR to SEK'].astype('float'))
        return df_out

    def src_read(self):
        """
        Read the intrastat source file into a dataframe.

        url: The url of the intrastat source file.
        """
        # Read data into pandas dataframe.
        with urllib.request.urlopen(self.src_url) as cc_url:
            try:
                df = pd.read_excel(cc_url.read())
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    print('Error: Requested commodity code url is invalid.')
                else:
                    print('Message: Requested commodity code url is valid.')
        return df



        df = pd.read_excel(input_file_name, dtype = str)
        try:
            # If file is read into data frame print confirmation.
            print('\n\nMessage: Source data successfully read.\n')
            print('3. Intrastat Source File')
        except pd.errors.ParserError:
            # If file is not read into data frame print error.
            print('Error: Source data could not be read.\n')
        return df
