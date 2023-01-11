"""

WELCOME TO MY FIRST DATA ENGINERRING ETL PIPELINE! 

See below regarding the various steps we've defined to get to  :
    
    1) We first import the necessary libraries and functions for our project.
    2) We then create a couple of variables to define the api we're going to call 
    as well as where we're looking to export our final transformed file.
    3) We then call the API (with the requests library) about the US population over the years
    and check whether the call has been successfull (with the api_answer function)
    4) Export the API answer's text data, convert it to a pandas dataframe 
    and apply a couple of transformation with the extract_data_into_dataframe function.
    5) Finally we export our transformed pandas dataframe to a CSV file to a local folder.
    
"""


#Importing the necessary libraries and functions (from functions.py) for our transformations.
import requests
import json
import pandas as pd

# Importing our transformation functions from the functions.py file
from functions import api_answer, extract_data_into_dataframe, push_dataframe_to_csv
from pathlib import Path  


#API we're looking to pull data from.
api = 'https://datausa.io/api/data?drilldowns=Nation&measures=Population' 
# Our path's destination.
path = '/Users/macbook/Documents/Github/Data-Engineering/us_population.csv'



def main():
    
    response_API = requests.get(api) # Calling the API
    api_answer(response_API.status_code) # Checking whether we've made a successfull call.
    output = extract_data_into_dataframe(response = response_API) # Uploading the data into a pandas dataframe
    push_dataframe_to_csv(dataframe = output, filepath = path) # Exporting the data to a csv file.

if __name__ == "__main__":
    main()






 
  



