"""
Foreign exchange rate resource component.
"""
import pandas as pd # Data analysis library.
import numpy as np # Array and matrice libary
import ssl # Secure sockets layer package.
import urllib.request # Url request handling module.
import urllib.error # Url request handling module.
import sys # Runtime environment handling module.
import xml.etree.ElementTree as et # XML parsing library.
import datetime as dt # Datetime parsing library.


class FxRates():
    """
    Read, transform and export fx rates from requested url.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for FxRates class.
        """
        # Disable security certificate checks for url requests.
        ssl._create_default_https_context = ssl._create_unverified_context


    def fx_parse_xml(self, xml_object : str, xml_child : str, xml_namespaces : str):
        """"
        Parse xml content and read into dataframe.

        :xml_tree: The tree of the xml object.
        :xml_root: The root of the xml object.
        :xml_namespaces: The namespaces of the xml object.
        """
        xml_tree = et.parse(xml_object)
        xml_root = xml_tree.getroot()
        # Find required child element instances and store content via list comprehension.
        rows = xml_root.findall(xml_child, namespaces=xml_namespaces)
        xml_data = [[row.get('time'), row.get('currency'), row.get('rate')] for row in rows]
        # Create columns for dataframe and read in content.
        data_frame = pd.DataFrame(xml_data, columns = ['Date', 'Currency', 'Rate'])
        return data_frame

    def read(self, url: str, xml_child : str, xml_namespaces : str):
        """
        Read commodity list url content into dataframe.

        :url: The url of the commodity code resource.
        """
        # Read data into pandas dataframe.
        xml_object = []
        with urllib.request.urlopen(url) as fx_url:
            try:
                xml_object = fx_url.read()
            except urllib.error.HTTPError as e_code:
                if e_code.code == 404:
                    print('Error: Requested commodity code url is invalid.')
                else:
                    print('Message: Requested commodity code url is valid.')
                    data_frame = self.fx_parse_xml(xml_object, xml_child, xml_namespaces)
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
