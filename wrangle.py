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

# Weather Cleaning
'''
This function will drop unneccessary columns, 
change datetime to a pandas datetime datatype,
and rename columns to be more readable to return
a clean dataframe.  
'''
def wrangle_weather():
    #read csv and turn into pandas dataframe
    weather = pd.read_csv('med_center_weather.csv')
    #drop columns we will not be using
    weather.drop(columns=[
    'Sensor_id', 
    'Vendor', 
    'SensorModel', 
    'LAT', 
    'LONG', 
    'Zone', 
    'AlertTriggered', 
    'SensorStatus'], inplace=True)
    #change datetime to pandas datetime object
    weather.DateTime = pd.to_datetime(weather.DateTime)
    #rename columns to be more readable
    weather = weather.rename(columns={"DateTime": "datetime", 
                            "Temp_C": "celsius", 
                            "Temp_F": "farenheit", 
                            "Humidity": "humidity",
                            "DewPoint_C": "dewpoint_celsius",
                            "DewPoint_F": "dewpoint_farenheit",
                            "Pressure_Pa": "pressure"})
    #return clean weather df
    return weather