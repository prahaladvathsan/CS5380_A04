import requests  
from bs4 import BeautifulSoup
import os  
import random  
import pandas as pd  
import numpy as np
import yaml  

# Suppress warnings for cleaner output
import warnings
warnings.filterwarnings('ignore')

# Define the main function
def fetch_weather_data():
    # Load parameters from the YAML configuration file
    config_params = yaml.safe_load(open("params.yaml"))["download"]

    # Construct the URL from parameters
    year_path = str(config_params['year']) + '/'
    location_file = str(config_params['n_loc']) + '.csv'
    base_url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/'

    # Combine parts to form the complete URL to download the data
    complete_url = os.path.join(base_url, year_path, location_file)
    
    # Perform the HTTP GET request to fetch the data
    data_response = requests.get(complete_url)

    # Define the name and path for the local file to save the data
    local_data_filename = 'weatherdata.csv'
    data_directory = 'data'

    # Ensure the directory exists
    os.makedirs(data_directory, exist_ok=True)
    
    # Write the content to a local file
    with open(os.path.join(data_directory, local_data_filename), 'wb') as file:
        file.write(data_response.content)

# Check if the script is executed directly (i.e., not imported)
if __name__ == "__main__":
    # Call the main function to execute the script
    fetch_weather_data()
