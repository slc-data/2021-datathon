# This PY file Contains all Code snippets we think would be beneficial to start using.

import pandas as pd
import numpy as np

# turn off pink warning boxes
import warnings
warnings.filterwarnings("ignore")

import sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
#-----------------------------------------------------------------------------

# This function will also feed into the second function. Without the second funciton this will not work.
    # The benefit of changing the dates this way is it will allow for a way to use saws in conjunction with outher data s3ets
        # such as COSA, Edwards Aquifer, and CPS
def fix_dates(df):
    '''Function to fix year month column into
    datetime.  Adds arbitraty day. but keeps 
    the same month and year.'''
    df['datetime'] = '01-20' + df['year_month']
    df.datetime = pd.to_datetime(df.datetime)
    return df

# This function will completely redo the formatting for saws
    # We decided to do this because breaking times into columns makes it hard to:
        # do time series analysis
        # find trends
        # ect.
    # This will make it to where there is a year month column, a record number column, location column, and gallons consumed.
# We highly suggest using this formatting so you can merge other data information on with ease, and be able to do a full analysis.
def reformat_saws():
    '''This function will drop unnecessary columns, 
    create a 'location' using data acquired from 
    other columns, and melt the data to make month year column'''
    # Reads the csv
    df = pd.read_csv('med_center_df.csv')
    # Removes NaN values from 'Prefix' and 'Suffix' column for concatenation in 'location'
    df['Prefix'] = df.Prefix.fillna(value = '')
    df['Suffix'] = df.Suffix.fillna(value = '')
    # Concatenating columns together for specific location
    df['location'] = df['Prefix'] + ' ' + df['Service Location'] + ' ' + df['Suffix']
    # Stripping any extra whitespace
    df['location'] = df.location.str.strip()
    df = df.drop(columns=['Unnamed: 0', 'Prefix', 'Suffix', 'Service Location'])
    df = df.melt(id_vars=['Record #', 'ZIP Code', 'location'], 
              var_name='Month & Year', value_name='Gallons Consumed')
    df = df.set_index('Record #')
    df = df.fillna(0)
    df = df.rename(columns={"ZIP Code": "zipcode", 'Month & Year':'year_month', 
                                'Gallons Consumed':'gallons_consumed'})
    # replace * with 0
    df = df.replace(to_replace='*', value=0)
    # change data type
    df['gallons_consumed'] = df['gallons_consumed'].astype(int)

    return fix_dates(df)