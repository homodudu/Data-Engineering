"""
Combined 8-digit nomenclature (Intrastat commodity code) module.
"""
import json # Json parsing module.
import requests # API request handling module.
import pandas as pd # Data analysis package.

API_URL = 'https://www.trade-tariff.service.gov.uk/api/v2/commodities/'
COLUMNS_RESP = ["CN8","Response Code", "Valid", "Description", "SU"]

class cn8():
    """
    Class that enables verification checks through an API on a given list of commodity codes.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for CN8 class.
        """
        pass

    def _get_response(self, cn8:str):
        """
        Get commodity code response from API.\n
        cn8: The 8 digit combined nomenclature to be analysed.
        """
        # Format input data to 8-digit commodity code.
        cn8 = str(cn8)[:8:]
        cn8 = cn8.ljust(8, '0')
        # Commodity API requires 10 digit query ID. Append suffixes to query string.
        cn8_suffix = ('00','10','20','30','40','50','60','70','80','90','99','XX')
        # Send request to API.
        response_check = True
        while(response_check):
            for i in range(0,len(cn8_suffix)):
                # Test suffixes until 10 digit commodity query is identified.
                response_API = requests.get(API_URL + cn8 + cn8_suffix[i])
                if response_API.status_code == 200:
                    response_check = False
                    break
                # 'XX' - default suffix for unidentified commodity queries.
                elif cn8_suffix[i] == 'XX':
                    response_check = False
                    break
        return response_API

    def _get_description(self, json_file:json):
        """
        Get commodity code description from json response.\n
        json_file: The json file to be parsed into data frame.
        """
        #Read 'data' section into data frame.
        data = json_file["data"]
        df = pd.DataFrame.from_dict(data)
        description = df["attributes"].loc["formatted_description"]
        return description

    def _get_supplementary(self, json_file :json):
        """
        Get commodity code supplementary unit from json response.\n
        json_file: The json file to be parsed into data frame.
        """
        # Read 'included' section into data frame.
        included = json_file["included"]
        df = pd.DataFrame.from_dict(included)
        # Filter through data to extract supplementary unit.
        df = df.loc[(lambda x : x["type"] == "duty_expression")]
        df = pd.DataFrame(df["attributes"].tolist())
        df = df.loc[lambda x : ~x["formatted_base"].str.contains('span')]
        df = df.loc[lambda x : x["base"] != '']
        # Assign hyphen symbol to commodities without supplementary unit.
        su = '-' if df.empty else df["base"].iloc[0]
        return su

    def _api_request(self, cn8:str):
        """
        Request commodity code API response.\n
        cn8: The 8-digit combined nomenclature to be analysed.
        """
        # Send API request.
        response_API = self._get_response(cn8)
        # Analyse status code.
        if response_API.status_code == 200:
            message = True
            json_file = json.loads(response_API.text)
            description = self._get_description(json_file)
            su = self._get_supplementary(json_file)
        elif response_API.status_code == 404:
            message = False
            description = 'Invalid commodity code - no description'
            su = None
        else:
            message = False
            description = 'Unexpected request error'
            su = None

        # Store response results in list.
        data = [cn8,response_API.status_code,message,description,su]
        return data

    def check(self, df:pd.DataFrame, column_name:str):
        """
        Check CN8 values by sending request to API client.\n
        df: The data frame containing a commodity code column.
        column_name: The column containing commodity codes to be analysed.
        """
        # Run validity check on unique rows to reduce API overhead.
        data = [self._api_request(c) for c in df[column_name].drop_duplicates()]
        df_response = pd.DataFrame(data,columns=COLUMNS_RESP)
        # Append unique API responses to original duplicates. Match by CN8 code.
        df_out = pd.merge(df, df_response, left_on=column_name, right_on=COLUMNS_RESP[0])
        if df_out.shape[0] > df.shape[0]:
            df_out.drop_duplicates(inplace=True)
            df_out.reset_index(drop=True, inplace=True)
        return df_out

def main():
    data = ['46012110','46012110','61041990','40151200','01022910','22021000','99999999']
    df = pd.DataFrame(data,columns=['CC'])
    print(cn8().check(df,'CC'))

if __name__ == '__main__':
    main()
