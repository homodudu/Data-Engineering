"""
Foreign exchange rate resource component.
"""
import ssl # Secure sockets layer package.
import urllib.request # Url request handling module.
import urllib.error # Url request handling module.
import xml.etree.ElementTree as et # XML parsing library.
import pandas as pd # Data analysis library.
import intra.constants as cn

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

    def fx_parse_xml(self, xml_object : object, xml_child : str, xml_namespaces : str):
        """
        Parse xml content and read into dataframe.

        xml_tree: The tree of the xml object.
        xml_root: The root of the xml object.
        xml_namespaces: The namespaces of the xml object.
        """

        xml_tree = et.parse(xml_object)
        xml_root = xml_tree.getroot()
        # Find required child element instances and store content via list comprehension.
        rows = xml_root.findall(xml_child, namespaces=xml_namespaces)
        xml_data = [[row.get('time'), row.get('currency'), row.get('rate')] for row in rows]
        # Create columns for dataframe and read in content.
        df = pd.DataFrame(xml_data, columns = ['Date', 'Currency', 'Rate'])
        return df

    def fx_create_pivot(self, df: pd.DataFrame):
        """
        Create fx rate pivot table by date and currency.
        """
        df_out = pd.pivot_table(df, index='Date', columns='Currency', values='Rate')
        # Add weekend dates missing from period to the table index.
        max_date = df.iloc[1, df.columns.get_loc('Date')]
        min_date = df.iloc[-1, df.columns.get_loc('Date')]
        date_idx = pd.date_range(min_date, max_date)
        df_out.index = pd.DatetimeIndex(df_out.index)
        df_out = df_out.reindex(date_idx)
        # Fill forward missing weekend fx rate values.
        df_out = df_out.ffill(axis=0)
        df_out = df_out.sort_index(ascending=0)
        return df_out

    def read(self, url: str, xml_child : str, xml_namespaces : str):
        """
        Read fx rates from parsed xml into dataframe.

        url: The url of the fx rate resource.
        """
        # Read data into pandas dataframe.
        xml_object = []
        opener = urllib.request.build_opener()
        try:
            xml_object = opener.open(url)
            df = self.fx_parse_xml(xml_object, xml_child, xml_namespaces)
        except urllib.error.HTTPError as e_code:
            if e_code.code == 404:
                print('Error: Requested commodity code url is invalid.')
            else:
                print('Message: Requested commodity code url is valid.')
        return df

    def transform(self, df: pd.DataFrame):
        """
        Transorm data by filling empty fx dates, cleansing rows and converting into pivot table.
        df: The dataframe to be transformed.
        """
        df = df.ffill(axis=0)
        df = df.dropna()
        # Create fx.rate pivot table.
        df['Rate'] = pd.to_numeric(df['Rate'])
        df_out = self.fx_create_pivot(df)
        return df_out

    def export(self, df: pd.DataFrame):
        """
        Export transformed fx rate table to csv file.
        """
        df.index.name = 'Date'
        df.to_csv('ECB FX Rates.csv', index=True)

    def rte_process(self, url: str, xml_child:  str, xml_namespaces: str):
        """
        Run full read, transform, export process.
        """
        df_read = self.read(url, xml_child, xml_namespaces)
        df_transform = self.transform(df_read)
        self.export(df_transform)
        print(pd.read_csv('ECB FX Rates.csv', dtype=str))
        return df_transform

FxRates().rte_process(cn.FxRates.URL_USE, cn.FxRates.XML_CHILD, cn.FxRates.XML_NAMESPACES)
