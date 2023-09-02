"""
Intrastat is a system that collects information relating to the trade of goods.
This script will prepare sample data from a fictious company into a submissable Swedish declaration.
"""
import pandas as pd # Data analysis library.
import _v2.cn8 as cn # Commodity code utility module.
import _v2.vies as vs  # VIES utility module.
import _v2.ecb as ec # ECB rate utility module.
import _v2.intra as it # Intrastat utility module.

# Read intrastat sample to data frame.
df = pd.read_excel('intrastat/_resources/Intrastat Data Sample.xlsx')

print('1. Input file:\n')
print(df)

# Transform mass, country code and mode of transport.
df['MASS'] = df['Mass (grams)'].astype(float)*0.001
df = it.iso().country_to_iso2(df,df['Country of Origin'])
df = df.rename(columns={'ISO2': 'COO'})
df = it.mot().check(df,'Mode of Transport')

# Analyse VAT codes.
df.loc[df['Transaction'] == 'B2C','Partner VAT'] = 'QV999999999999'
df_vies = vs.vies().check(df, 'Partner VAT')
print('2. Vies check:\n')
print(df_vies)

# Analyse commodity codes.
df = cn.cn8().check(df,'Commodity Code')

# FX rate conversion.
df['Shipping Date'] = pd.to_datetime(df['Shipping Date'])
df_ecb = ec.ecb().get_rates('2022-01-01')['SEK']
df = pd.merge(left=df, right=df_ecb, left_on='Shipping Date', right_index=True, how='left')
df['NET'] = df['Net (EUR)'].astype(float)*df['SEK'].astype(float)
df['NET'] = round(df['NET'],2)

# Create declaration output.
columns = ['CN8', 'Ship To', 'COO','MOT',
        'Incoterms', 'NET', 'MASS', 'Quantity','Partner VAT']
df = df[columns]
print('3. Output file:\n')
print(df)
