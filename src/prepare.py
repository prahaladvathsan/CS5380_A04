import pandas as pd
import numpy as np
import random
import yaml
import sys

import warnings
warnings.filterwarnings('ignore')  # Ignore warnings

def main():
    # Load parameters from yaml file
    params = yaml.safe_load(open("params.yaml"))["prepare"]

    # Get seed, input and output paths from parameters
    seed = params['seed']
    in_path = sys.argv[1]
    out_path = sys.argv[2]

    # Set the seed for random number generation
    random.seed(seed)

    # Load the data from the CSV file
    df = pd.read_csv(in_path)
    # Convert the 'DATE' column to datetime format
    df['DATE'] = pd.to_datetime(df['DATE'])

    # Get the column names that contain 'monthly' and have non-null values
    monthly_cols = [col for col in df.columns if 'monthly' in col.lower() and ~df[col].isna().all()]
    # Get the column names that contain 'daily' and have non-null values
    daily_cols = [col for col in df.columns if 'daily' in col.lower() and ~df[col].isna().all()]

    # Remove the 'Monthly' prefix from the column names
    vars_monthly = [col.replace('Monthly','') for col in monthly_cols]
    # Remove the 'Daily' prefix from the column names
    vars_daily = [col.replace('Daily','') for col in daily_cols]

    # Get the intersection of the daily and monthly variables
    vars = list(set(vars_daily).intersection(set(vars_monthly)))

    # Add a 'month' column to the dataframe
    df['month'] = df['DATE'].dt.month

    values = []
    for variable in vars:
        # Drop rows with null values in the 'Monthly' + variable column
        df_temp = df[['month','Monthly'+variable]].dropna()
        # Calculate the mean of the 'Monthly' + variable column for each month
        temp = df_temp.groupby(['month'])['Monthly'+variable].mean()
        temp.index.name = None
        values.append(temp.values)

    # Convert the list of values to a dataframe and write it to a CSV file
    values_df = pd.DataFrame(values).T
    values_df.to_csv(out_path,index=True)

    # Write the variable names to a text file
    with open('data/variable.txt','w') as f:
        for variable in vars:
            f.write(variable+' ')

if __name__ == "__main__":
    # Run the main function if the script is run directly
    main()