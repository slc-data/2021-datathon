import pandas as pd
import numpy as np

#-----------------------------------------------------------------------------

# Air Quality Cleaning

def clean_air(df):
    '''Drops unneeded columns from the air quality df
    then handles the nulls in alert triggered column'''
    # drop the colums
    df = df.drop(columns=['LAT', 'LONG', 'Zone', 
                      'Sensor_id', 'SensorModel', 
                      'SensorStatus'])
    df.fillna("None", inplace = True)
    # return new df
    return df


#-----------------------------------------------------------------------------