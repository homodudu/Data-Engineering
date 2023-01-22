"""
Commodity code resource component.
"""
import ssl # Secure sockets layer package.
import urllib.request # Url request handling module.
import urllib.error # Url request handling module.
import pandas as pd # Data analysis package.


class CommodityCodes():
    """
    Read, transform and export commodity codes from requested url.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for CommodityCodes class.
        """
        # Disable security certificate checks for url requests.
        ssl._create_default_https_context = ssl._create_unverified_context

    def read(self, url: str):
        """
        Read commodity list url content into dataframe.

        :url: The url of the commodity code resource.
        """
        # Read data into pandas dataframe.
        with urllib.request.urlopen(url) as cc_url:
            try:
                data_frame = pd.read_excel(cc_url.read())
            except urllib.error.HTTPError as e_code:
                if e_code.code == 404:
                    print('Error: Requested commodity code url is invalid.')
                else:
                    print('Message: Requested commodity code url is valid.')
        return data_frame

    def transform(self, data_frame: pd.DataFrame):
        """
        Transform commodity code data into lookup table format.
        """
        # Pad left first column to CN8 format
        data_frame.iloc[:,0] = data_frame.iloc[:,0].astype("str")
        data_frame.iloc[:,0] = data_frame.iloc[:,0].str.pad(8, side='left', fillchar='0')
        # Rename first column to CN8.
        data_frame.columns.values[0] = 'CN8'
        return data_frame

    def export(self, data_frame: pd.DataFrame):
        """
        Export transformed commodity code table to csv file.
        """
        data_frame.to_csv('CN8 Codes.csv', index=False)

    def rte_process(self, url : str):
        """
        Run full read, transform, export process.
        """
        df_read = self.read(url)
        df_transform = self.transform(df_read)
        self.export(df_transform)
        print(pd.read_csv('CN8 Codes.csv', dtype=str))
        return df_transform
