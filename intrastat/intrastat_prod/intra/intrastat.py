"""
Intrastat data processing component.
"""

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
