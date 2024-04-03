import pandas as pd
import numpy as np
import os
import sys

import warnings
warnings.filterwarnings('ignore')  # Ignore warnings

def main():
    # Get input and output file paths from command line arguments
    in_path = sys.argv[1]
    out_path = sys.argv[2]

    # Load the data from the CSV file
    df = pd.read_csv(in_path)
    # Convert the 'DATE' column to datetime format
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Read the variable names from a text file
    with open('data/variable.txt','r') as f:
        file_contents = f.read()
        vars = file_contents.split()

    # Add a 'month' column to the dataframe
    df['month'] = df['DATE'].dt.month
    values = []
    for variable in vars:
        # Drop rows with null values in the 'Daily' + variable column
        df_temp = df[['month','Daily'+variable]].dropna()
        # Calculate the mean of the 'Daily' + variable column for each month
        temp = df_temp.groupby(['month'])['Daily'+variable].mean()
        temp.index.name = None
        values.append(temp.values)

    # Convert the list of values to a dataframe and write it to a CSV file
    values_df = pd.DataFrame(values).T
    values_df.to_csv(out_path,index=True)

if __name__ == '__main__':
    # Run the main function if the script is run directly
    main()