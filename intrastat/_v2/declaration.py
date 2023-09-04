"""
Intrastat is a system that collects information relating to the trade of goods.
This script will prepare sample data from a fictitious company into a submissable Swedish declaration.
"""
import pandas as pd # Data analysis library.
import _v2.cn8 as cn # Commodity code utility module.
import _v2.vies as vs  # VIES utility module.
import _v2.ecb as ec # ECB rate utility module.
import _v2.intra as it # Intrastat utility module.

INPUT_FILE = 'intrastat/_resources/Intrastat Data Sample.xlsx'
OUTPUT_FILE = 'intrastat/_v2/Intrastat Declaration Sample.xlsx'


def rate(input_file, output_file):
    """
    Run the complete intrastat data preparation process.\n
    input_file: The filepath where the source data will be read from.
    output_file: The filepath where the prepared data will be written to.\n
    This function reads and writes excel files only.
    """
    # Read intrastat sample to data frame.
    df = pd.read_excel(input_file)
    print('\n1. Input file:\n')
    print(df)

    # Analyse VAT codes.
    df.loc[df['Transaction'] == 'B2C','Partner VAT'] = 'QV999999999999'
    df_vies = vs.vies().check(df, 'Partner VAT')
    print('\n2. Vies check:\n')
    print(df_vies)

    # Analyse commodity codes.
    df = cn.cn8().check(df,'Commodity Code')
    print('\n3. Cn8 check:\n')
    print(df)

    # Analyse reporting currency.
    df['Shipping Date'] = pd.to_datetime(df['Shipping Date'])
    df_ecb = ec.ecb().get_rates('2022-01-01')['SEK']
    df = pd.merge(left=df, right=df_ecb, left_on='Shipping Date', right_index=True, how='left')
    df['Net (SEK)'] = df['Net (EUR)'].astype(float)*df['SEK'].astype(float)
    df['Net (SEK)'] = round(df['Net (SEK)'],2)
    print('\n4. FX rate check:\n')
    print(df[['Net (EUR)','SEK','Net (SEK)']])

    # Transform mass, country code and mode of transport.
    df['MASS'] = df['Mass (grams)'].astype(float)*0.001
    df = it.iso().country_to_iso2(df,df['Country of Origin'])
    df = df.rename(columns={'ISO2': 'COO'})
    df = it.mot().check(df,'Mode of Transport')

    # Export declaration output.
    columns = ['CN8', 'Ship To', 'COO','MOT','Incoterms', 'Net (SEK)', 'MASS', 'Quantity','Partner VAT']
    df = df[columns]
    df.iloc[:,0] = df.iloc[:,0].astype("str")
    df.to_excel(output_file, index=False)
    print('\n5. Output file:\n')
    print(df)
    return df

def main():
    rate(INPUT_FILE, OUTPUT_FILE)

if __name__ == '__main__':
    main()
