import pandas as pd
import numpy as np

#-----------------------------------------------------------------------------

# Air Quality Cleaning

def clean_air(df):
    '''Drops unneeded columns from the air quality df
    then handles the nulls in alert triggered column
    set to date time format'''
    # drop the colums
    df = df.drop(columns=['LAT', 'LONG', 'Zone', 
                      'Sensor_id', 'SensorModel', 
                      'SensorStatus'])
    # replace nulls in ALertTriggered to None
    df.fillna("None", inplace = True)
    # set to date time format
    df.DateTime = pd.to_datetime(df.DateTime)
    # return new df
    return df

#-----------------------------------------------------------------------------

# Flood Cleaning

def clean_flood(df):
    '''Drops unneeded columns from the med center flooding df
    Makes sure DateTime is in DateTime format'''
    # drop the colums
    df = df.drop(columns=['LAT', 'LONG', 'Zone', 
                          'Sensor_id', 'SensorModel', 
                          'SensorStatus', 'AlertTriggered', 
                          'Temp_C', 'Temp_F', 'Vendor'])
    # Set to date time format
    df.DateTime = pd.to_datetime(df.DateTime)
    # return new df
    return df

#-----------------------------------------------------------------------------