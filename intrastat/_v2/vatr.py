"""
VAT rate lookup module.
"""
import html5lib # HTML parsing module
import lxml # Markup language processing module.
import ssl # Secure sockets layer module.
import re # Regex module.
import json # Json parsing module.
import requests # API request handling module.
import pandas as pd # Data analysis package.

URL = 'https://europa.eu/youreurope/business/taxation/vat/vat-rules-rates/'
COLUMNS_RESP = ['Member State', 'Country code', 'Standard rate', 'Reduced rate 1',
        'Reduced rate 2','Super reduced rate']

# Disable security certificate checks for url requests.
ssl._create_default_https_context = ssl._create_unverified_context

class vatr():
    """
    Class that retrieves current VAT rates published by EU commision.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for VATR class.
        """
        pass

    def _read(self, url:str):
        """
        Read html content into dataframe.\n
        url: The html resource to read.
        """
        # Read html content.
        ssl._create_default_https_context = ssl._create_unverified_context
        df = pd.read_html(url)[0]
        df.rename(columns=df.iloc[1], inplace=True)
        # Split RR column to separate RR1 and RR2 columns.
        df[['Reduced rate 2','Reduced rate 1']] = df.iloc[:,3].str.split('/',expand=True)
        df[df.columns] = df.apply(lambda x: x.str.strip())
        df['Reduced rate 1'] = df['Reduced rate 1'].astype(str)
        # Sort RR columns so that RR1 stores the higher reduced value.
        df.loc[df['Reduced rate 1'] == 'None','Reduced rate 1'] = df['Reduced rate 2']
        df.loc[df['Reduced rate 1'] == '-','Reduced rate 1'] = df['Reduced rate 2']
        df.loc[df['Reduced rate 2'] == df['Reduced rate 1'],'Reduced rate 2'] = '-'
        # Format output table.
        df = df.iloc[2:]
        df.reset_index(inplace=True)
        df = df[COLUMNS_RESP]
        return df

    def check(self,*country):
        """
        Check the current VAT rate.\n
        country: The country to check.\n
        1. Country code must be given as ISO 3166 country name or Alpha-2:
        2. If no country has been provided, a complete table of EU rates is returned.
        """
        # Cleanse country input string
        country = re.sub("\W","",str(country))
        df = self._read(URL)
        # Filter return data by country input parameters.
        if len(country) == 2:
            df = df.loc[df['Country code'] == country]
        elif len(country) > 2:
            df = df.loc[df['Member State'] == country]
        else: df
        return df

def main():
    print(vatr().check())

if __name__ == '__main__':
    main()
