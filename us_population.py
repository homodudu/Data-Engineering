import requests
import json
import pandas as pd

# Pull data from api.
response_API = requests.get('https://datausa.io/api/data?drilldowns=Nation&measures=Population')
print(response_API.status_code)
data = response_API.text

# Parse to json file. Store data in list. 
json_file = json.loads(data)
list = json_file["data"]

# Sort data by ascending year.
list.sort(key=lambda x: x["Year"])

# Convert list to dictionary.
dict = {}
for x in range(0, len(list)) :
    dict[x] = list[x]

# Dictionary converted and exported to tablature format using pandas. 
from pathlib import Path  
filepath = Path('/Users/macbook/Documents/Github/Data-Engineering/us_population.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
pd.DataFrame.from_dict(data=dict,orient='index').to_csv(filepath, header=True)



 
  



