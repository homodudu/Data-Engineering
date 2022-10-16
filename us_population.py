import requests
import json
import pandas as pd

response_API = requests.get('https://datausa.io/api/data?drilldowns=Nation&measures=Population')
#print(response_API.status_code)
data = response_API.text
json_file = json.loads(data)
list = json_file["data"]
dict = {}

list.sort(key=lambda x: x["Year"])

for x in range(0, len(list)) :
    dict[x] = list[x]

from pathlib import Path  
filepath = Path('/Users/macbook/Documents/Github/Data-Engineering/us_population/us_population.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
pd.DataFrame.from_dict(data=dict,orient='index').to_csv(filepath, header=True)



 
  



