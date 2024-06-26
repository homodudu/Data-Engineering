"""
ISO country code module.
"""
import pandas as pd # Data analysis package.
import requests # API request handling module.
import json # Json parsing module.

API_URL = 'https://restcountries.com/v3.1/all'
COLUMNS_RESP = ["common","official", "cca2", "cca3","continents"]

class iso():
    """
    Class that contains functions to check country code.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for class.
        """
        pass

    def _api_request(self):
        """
        Request ISO code API response\n
        GB is defined as ISO code XU for intrastat purposes.
        """
        # Send API request.
        response_API = requests.get(API_URL)
        json_file = json.loads(response_API.text)
        data = pd.DataFrame.from_dict(json_file)

        # Transform response and store in lookup table.
        data['common'] = [x['common'] for x in data['name']]
        data['official'] = [x['official'] for x in data['name']]
        df = pd.DataFrame(data,columns=COLUMNS_RESP)
        df['continents'] = [x[0] for x in df['continents']]
        df['cca2'] = df['cca2'].replace('GB','XU')
        return df

    def country_to_iso2(self, df, column_name):
        """
        Translate country name to ISO-2 equivalent. Append result.\n
        df: The data frame containing a country column.
        column_name: The column containing the country name to be analysed.
        """
        # Retrieve country code lookup table.
        df_out = self._api_request()[['common','cca2']]
        df_out = pd.merge(df, df_out, left_on=column_name, right_on='common', how='left')
        df_out.drop('common', axis=1, inplace=True)
        df_out = df_out.rename(columns={'cca2': 'ISO2'})
        return df_out

    def alpha3_to_iso2(self, df, column_name):
        """
        Translate alpha3 country code to ISO-2 equivalent. Append result.\n
        df: The data frame containing a country code.
        column_name: The column containing the country code to be analysed.
        """
        # Retrieve country code lookup table.
        df_out = self._api_request()[['cca3','cca2']]
        # Match by key column. Return original and value columns only.
        df_out = pd.merge(df, df_out, left_on=column_name, right_on='cca3', how='left')
        df_out.drop('cca3', axis=1, inplace=True)
        df_out = df_out.rename(columns={'cca2': 'ISO2'})
        return df_out

    def alpha2_to_iso2(self, df, column_name):
        """
        Translate alpha2 country code to intrastat ISO-2 equivalent. Append result.\n
        df: The data frame containing a country code.
        column_name: The column containing the country code to be analysed.\n
        Certain country codes have intrastat specific translations such as GB -> XU.
        """
        # Translate GB intrastat code manually. Does not adopt ISO standard.
        df[column_name] = df[column_name].replace(regex="UK|GB", value='XU')
        # Translate RS intrastat code manually. Does not adopt ISO standard.
        df[column_name] = df[column_name].replace(regex="RS", value='XS')
        # Retrieve country code lookup table.
        df_out = self._api_request()['cca2']
        # Match by key column. Return original and value columns only.
        df_out = pd.merge(df, df_out, left_on=column_name, right_on='cca2', how='left')
        df_out = df_out.rename(columns={'cca2': 'ISO2'})
        return df_out

def main():
    data = ['Spain','France','Italy','United Kingdom','Slovenia']
    df = pd.DataFrame(data,columns=['Country'])
    print(iso().country_to_iso2(df,'Country'))

if __name__ == '__main__':
    main()
