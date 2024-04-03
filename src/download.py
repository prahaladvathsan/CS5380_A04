import requests
from bs4 import BeautifulSoup
import os
import random
import pandas as pd
import numpy as np
import yaml

import warnings
warnings.filterwarnings('ignore')  # Ignore warnings

def main():
    # Load parameters from yaml file
    params = yaml.safe_load(open("params.yaml"))["download"]

    # Get year and location from parameters
    year = str(params['year'])+'/'
    n_loc = str(params['n_loc'])+'.csv'

    # Base URL for data
    url = 'https://www.ncei.noaa.gov/data/local-climatological-data/access/'

    # Construct the URL by joining the base URL, year and location
    main_url = os.path.join(url,year,n_loc)
    
    # Send a GET request to the URL
    response = requests.get(main_url)

    # Define the local filename where data will be saved
    local_filename = 'weatherData.csv'

    # Create a directory named 'data' if it doesn't exist
    os.makedirs('data',exist_ok=True)
    
    # Write the content of the response to a CSV file
    open(os.path.join('data',local_filename),'wb').write(response.content)
    
if __name__ == "__main__":
    # Run the main function if the script is run directly
    main()