"""
Intrastat utility module.
"""
import pandas as pd # Data analysis package.
import requests # API request handling module.
import json # Json parsing module.

class mot():
    """
    Class that contains functions to check mode of transport.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for class.
        """
        pass

    def check(self, df:pd.DataFrame, column_name:str):
        """
        Translate mode of transport values to intrastat integer value.\n
        df: The data frame containing a the mode of transport column.
        column_name: The column containing commodity codes to be analysed.
        """
        # Create mode of transport lookup table.
        df_mot = pd.DataFrame({'Type': ['Sea','Rail','Road','Air'], 'MOT': ['1','2','3','4']})
        # Match by key column. Return original and value columns only.
        df = pd.merge(df, df_mot, left_on=column_name, right_on='Type', how='left')
        df.drop('Type', axis=1, inplace=True)
        return df

def main():
    pass

if __name__ == '__main__':
    main()
