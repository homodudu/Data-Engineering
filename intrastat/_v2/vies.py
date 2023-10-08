"""
VAT number identification (VIES) module.
"""
import json # Json parsing module.
import requests # API request handling module.
import pandas as pd # Data analysis package.

API_URL = 'https://ec.europa.eu/taxation_customs/vies/rest-api/ms/'
COLUMNS_RESP = ["Vat Number","Response Code", "Valid",
                "Description","Company", "Address","Request Date"]

class vies():
    """
    Class that enables verification checks through an API on a given list of VAT ID's.
    """
    def __init__(self):
        """
        Constructor (initialise attributes) for VIES class.
        """
        pass

    def _api_request(self, vat:str):
        """
        Request commodity code API response.\n
        vat: The VATID to be analysed.
        """
        # Format VATID and components.
        vat = str(vat)
        vat_no = vat[2::]
        alpha2 = vat[:2:]
        # Send API request.
        response_API = requests.get(API_URL + alpha2 + '/vat/' + vat_no)
        data = json.loads(response_API.text)
        description = ''
        # Analyse status code.
        if response_API.status_code == 200 and data['isValid']:
            description = 'OK - Valid VAT number'
        elif response_API.status_code == 200 and not data['isValid']:
            description = 'Warning - invalid VAT number'
        else: description = ("Error - unexpected request issue.")
        # Store response results in list.
        data = [data['vatNumber'],response_API.status_code,data['isValid']
                ,description,data['name'],data['address'], data['requestDate'][:10:]]
        return data

    def check(self, df:pd.DataFrame, column_name:str):
        """
        Check VATID values by sending request to API client.\n
        df: The data frame containing a commodity code column.
        column_name: The column containing commodity codes to be analysed.
        """
        # Run validity check on unique rows to reduce API overhead.
        data = [self._api_request(v) for v in df[column_name].drop_duplicates()]
        df_response = pd.DataFrame(data,columns=COLUMNS_RESP)
        # Append unique API responses to original duplicates. Match by VAT number.
        df['VAT NO'] = df[column_name].str[2:]
        df_out = pd.merge(df, df_response, left_on='VAT NO', right_on=COLUMNS_RESP[0], how='left')
        if df_out.shape[0] > df.shape[0]:
            df_out.drop_duplicates(inplace=True)
            df_out.reset_index(drop=True, inplace=True)
        df_out.drop('VAT NO', axis=1, inplace=True)
        return df_out

def main():
    data = ['ATU25700701','ATU25700701','SK2020229618','FI15601431','PL52200000XX']
    df = pd.DataFrame(data,columns=['VATID'])
    print(vies().check(df,'VATID'))

if __name__ == '__main__':
    main()
