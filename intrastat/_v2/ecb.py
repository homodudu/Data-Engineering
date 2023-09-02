"""
Foreign exchange rate (European Central Bank) module.
"""
import ssl # Secure sockets layer package.
import urllib.request # Url handling module.
import urllib.error # Url request handling module.
import xml.etree.ElementTree as et # XML parsing library.
import pandas as pd # Data analysis library.
import datetime as dt

ECB_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml'
XML_NAMESPACES = {'ex': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
XML_CHILD = './/ex:Cube'

class ecb():
    """
    Class that retrieves daily foreign exchange rate data from a URL.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for ECB class.
        """
        # Disable security certificate checks for url requests.
        ssl._create_default_https_context = ssl._create_unverified_context
        # Set default date filter range for ECB exchange rate request.
        self.end_date = dt.datetime.today()
        self.start_date = dt.datetime.today() - pd.DateOffset(years=1)

    def _parse(self):
        """
        Parse xml content and read into dataframe.
        """
        try:
            # Configure request parameters.
            opener = urllib.request.build_opener()
            xml_object = opener.open(ECB_URL)
            xml_tree = et.parse(xml_object)
            xml_root = xml_tree.getroot()
            # Find required child element instances and store content via list comprehension.
            rows = xml_root.findall(XML_CHILD, namespaces=XML_NAMESPACES)
            xml_data = [[row.get('time'), row.get('currency'), row.get('rate')] for row in rows]
            # Create columns for dataframe and read in content.
            df = pd.DataFrame(xml_data, columns = ['Date', 'Currency', 'Rate'])
        except et.ParseError:
            # Return empty dataframe if parse error.
            df = pd.DataFrame()
            raise('Error: Xml data parsing failed.')
        return df

    def _pivot(self, df: pd.DataFrame):
        """
        Create fx rate pivot table by date and currency.\n
        df: The dataframe to create pivot table from.
        """
        df_out = pd.pivot_table(df, index='Date', columns='Currency', values='Rate')
        # Add weekend dates missing from period to the table index.
        date_idx = pd.date_range(df["Date"].min(), df['Date'].max())
        df_out.index = pd.DatetimeIndex(df_out.index)
        df_out = df_out.reindex(date_idx)
        # Fill forward missing weekend fx rate values.
        df_out = df_out.ffill(axis=0)
        df_out = df_out.sort_index(ascending=0)
        return df_out

    def _transform(self):
        """
        Transform fx rates parsed from xml into dataframe.
        """
        # Read data into pandas dataframe.
        try:
            df = self._parse()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise('Error: Requested fx rate url is invalid.')
        #Cleanse rows.
        df = df.ffill(axis=0)
        df = df.dropna()
        # Create fx rate pivot.
        df['Rate'] = pd.to_numeric(df['Rate'])
        df_out = self._pivot(df)
        return df_out

    def get_rates(self, start_date=None, end_date=None):
        """
        Get ECB exchange rates from a specific period. \n
        start_date: The start date for the ECB exchange rate request.
        end_date: The end date for the ECB exchange rate request.\n
        1. Dates must be provided in "YYYY-MM-DD" format.
        2. If no date range provided, the previous year will be returned.
        """
        # Check if default start date needs applying, else parse input date.
        if start_date is None:
            start_date = self.start_date
        else:
           start_date = dt.datetime.strptime(start_date,'%Y-%m-%d')
        # Check if default end date needs applying, else parse input date.
        if end_date is None:
            end_date = self.end_date
        else:
           end_date = dt.datetime.strptime(end_date,'%Y-%m-%d')
        # Apply date filter range to transformed xml data.
        df_out = self._transform()
        df_out = df_out.loc[end_date:start_date]
        return df_out

def main():
    pass

if __name__ == '__main__':
    main()
