"""

Welcome to the functions.py file where we store our transformation functions.

"""

#Importing the necessary libraries for our transformations.
import pandas as pd
import json
import os

def api_answer(status_code):
    
    """
    This function informs us whether we've made a successfull API call by printing different messages 
    depending on the returned api status code (if it's 200 it's a successfull one, if not it's failed).
    """
    
    if status_code == 200:
        print('Succesfull API call! We can download the data..')
    else:
        print('The API call failed - the data is unavailable..')


def extract_data_into_dataframe(response):
    
    """
    With this function we extract the text data from the API and store it 
    into a pandas dataframe.
    """
    print('Uploading the API data into a pandas dataframe.')
    data = response.text # converting our api response into a text variable.

    # Parsing to a json file. Store data in list. 
    json_file = json.loads(data)
    list = json_file["data"]

    # Creating an empty dataframe and storing our data into it.
    output = pd.DataFrame()
    output = output.append(list, ignore_index=True)
    print('Operating a couple of transformation to our dataframe...')
    to_drop = ['ID Year','Slug Nation'] #Dropping the unecessary columns
    output.drop(to_drop, axis=1, inplace=True)
    output = output.sort_values(by=['Year'],ascending=False)
    print('\n')    
    print('Success the API data has been uploaded into the output dataframe.')

    return output


def push_dataframe_to_csv(dataframe,filepath):
    
    """
    In this function we'll pass the dataframe we've created with the previous function (output from extract_data_into_dataframe)
    and export it as a CSV file to our local drive.
    
    """
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    else:
        print('The filepath already exists...')
        
    dataframe.to_csv(filepath, header=True)
    print("Success! The dataframe has been exported!")
    
    
    