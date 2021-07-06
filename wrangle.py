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

def wrangle_weather():
    '''
    This function will drop unneccessary columns, 
    change datetime to a pandas datetime datatype,
    and rename columns to be more readable to return
    a clean dataframe.  
    '''
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

#-----------------------------------------------------------------------------

# Cleaning SAWS

def wrangle_saws():
    '''
    This function will drop unnecessary columns, 
    create a 'location' using data acquired from 
    other columns, and transpose the data so that each column 
    is an individual property, with rows that are dates,
    and a final row that specifies the area.
    '''
    # Reads the csv
    df = pd.read_csv('med_center_saws.csv', encoding = "utf-8")
    # Removes NaN values from 'Prefix' and 'Suffix' column for concatenation in 'location'
    df['Prefix'] = df.Prefix.fillna(value = '')
    df['Suffix'] = df.Suffix.fillna(value = '')
    # Concatenating columns together for specific location
    df['location'] = df['Prefix'] + ' ' + df['Service Location'] + ' ' + df['Suffix']
    # Stripping any extra whitespace
    df['location'] = df.location.str.strip()
    # Dropping columns
    df.drop(columns = ['Unnamed: 0', 'ZIP Code', 'Prefix', 'Service Location', 'Suffix'], inplace = True)
    # Resetting the index to be record numbers
    df = df.set_index('Record #')
    # Transposing the data
    df = df.T
    return df

#-----------------------------------------------------------------------------

# Sound Cleaning

def wrangle_sound():
    '''
    This function drops unnecessary columns and
    converts the 'DateTime' column to a datetime 
    object
    '''

    df = pd.read_csv('med_center_sound.csv')
    # Drops unnecessary columns
    df = df.drop(columns = ['SensorStatus', 'AlertTriggered', 'Zone', 'LONG', 
                            'LAT', 'SensorModel', 'Vendor', 'Sensor_id'])
    # Converts to datetime
    df['DateTime'] = pd.to_datetime(df.DateTime)
    return df