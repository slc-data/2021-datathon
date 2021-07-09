import pandas as pd
import numpy as np

# turn off pink warning boxes
import warnings
warnings.filterwarnings("ignore")

import sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
#-----------------------------------------------------------------------------

# Air Quality Cleaning
def clean_air():
    '''Drops unneeded columns from the air quality df
    then handles the nulls in alert triggered column
    set to date time format'''
    # read the csv
    air = pd.read_csv('med_center_air.csv')
    # drop the colums
    air = air.drop(columns=['LAT', 'LONG', 'Zone', 
                            'Sensor_id', 'SensorModel', 
                            'SensorStatus', 'Vendor'])
    # replace nulls in ALertTriggered to None
    air.fillna("None", inplace = True)
    # set to date time format
    air.DateTime = pd.to_datetime(air.DateTime)
    # rename features
    air = air.rename(columns={"DateTime": "datetime",
                              "AlertTriggered":"alert_triggered"})
    air = air.replace(to_replace=-999, value=0)
    # create time series features
    air['dates'] = pd.to_datetime(air['datetime']).dt.date
    air['time'] = pd.to_datetime(air['datetime']).dt.time
    air['hour'] = pd.to_datetime(air['datetime']).dt.hour
    air['weekday'] = pd.to_datetime(air['datetime']).dt.weekday
    # make all CO bins
    air['AQI_CO'] = pd.cut(air.CO, 
                            bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                            labels = ['Good', 'Moderate', 
                                      'Unhealthy for Sensitive Groups', "Unhealthy", 
                                      "Very Unhealthy", 'Hazardous'])
    
    CO_24hr = air.groupby('dates', as_index=False)['CO'].mean()
    CO_24hr = CO_24hr.rename(columns={'CO':'CO_24hr'})
    air = air.merge(CO_24hr, on = 'dates', how ='left')
    air['AQI_CO_24hr'] = pd.cut(air.CO_24hr, 
                                bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    
    pm_25_24hr = air.groupby('dates', as_index=False)['Pm2_5'].mean()
    pm_25_24hr = pm_25_24hr.rename(columns={'Pm2_5':'Pm_25_24hr'})
    air = air.merge(pm_25_24hr, on = 'dates', how ='left')
    air['AQI_pm_25_24hr'] = pd.cut(air.Pm_25_24hr, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    
    pm_10_24hr = air.groupby('dates', as_index=False)['Pm10'].mean()
    pm_10_24hr = pm_10_24hr.rename(columns={'Pm10':'Pm_10_24hr'})
    air = air.merge(pm_10_24hr, on = 'dates', how ='left')
    air['AQI_pm10_24hr'] = pd.cut(air.Pm_10_24hr, 
                                bins = [-1,55,154,255,355,425,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # return new df
    return air

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

# Wrangle SAWS

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
    # Remove any column that has more than 8 NaN values
    df = df.dropna(thresh=len(df) - 8, axis=1)
    return df

#-----------------------------------------------------------------------------

# Cleaning saws for analysis

def clean_saws(saws_df):
    '''
    This function converts index to datetime object,
    makes columns into strings instead of integers,
    replace '*' with zeroes, converts data into integers,
    and fills any NaNs with the average for that column
    '''
    # Drops the location row as it messes with calculation, can be added back later
    saws_df = saws_df.drop(['location'])
    # Fix formatting of datetime row
    saws_df.index = '20' + saws_df.index.str[0:2] + '-' + saws_df.index.str[3:] + '-' + '01'
    # Converting to a datetime object
    saws_df.index = pd.to_datetime(saws_df.index)
    # Converts column names to strings
    saws_df.columns = saws_df.columns.astype(str)
    # Replaces asterisks with stars
    saws_df = saws_df.replace('*', 0)
    # Changes data in the dataframe into integers
    saws_df = saws_df.apply(pd.to_numeric)
    # Replaces NaN values with average of that column
    saws_df = saws_df.fillna(saws_df.mean())
    return saws_df
    
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
    # make noise level feature
    df['noise_level'] = pd.cut(df.NoiseLevel_db, 
                                bins = [-1,46,66,81,101,4000],
                                labels = ['Normal', 'Moderate', 
                                          'Loud', "Very Loud", 
                                          "Extremely Loud"])
    return df

#-----------------------------------------------------------------------------

# Split the Data into Tain, Test, and Validate.
def split_data(df):
    '''This fuction takes in a df 
    splits into train, test, validate
    return: three pandas dataframes: train, validate, test
    '''
    # split the focused zillow data
    train_validate, test = train_test_split(df, test_size=.2, random_state=1234)
    train, validate = train_test_split(train_validate, test_size=.3, 
                                       random_state=1234)
    return train, validate, test

#-----------------------------------------------------------------------------

# Split the data into X_train, y_train, X_vlaidate, y_validate, X_train, and y_train
def split_train_validate_test(train, validate, test):
    ''' This function takes in train, validate and test
    splits them into X and y versions
    returns X_train, X_validate, X_test, y_train, y_validate, y_test'''
    X_train = train.drop(columns = ['level_of_success'])
    y_train = pd.DataFrame(train.level_of_success)
    X_validate = validate.drop(columns=['level_of_success'])
    y_validate = pd.DataFrame(validate.level_of_success)
    X_test = test.drop(columns=['level_of_success'])
    y_test = pd.DataFrame(test.level_of_success)
    return X_train, X_validate, X_test, y_train, y_validate, y_test

#-----------------------------------------------------------------------------

# Scale the Data
def scale_my_data(train, validate, test):
    scale_columns = []
    scaler = MinMaxScaler()
    scaler.fit(train[scale_columns])
    train_scaled = scaler.transform(train[scale_columns])
    validate_scaled = scaler.transform(validate[scale_columns])
    test_scaled = scaler.transform(test[scale_columns])
    #turn into dataframe
    train_scaled = pd.DataFrame(train_scaled)
    validate_scaled = pd.DataFrame(validate_scaled)
    test_scaled = pd.DataFrame(test_scaled)
    
    return train_scaled, validate_scaled, test_scaled

#-----------------------------------------------------------------------------
