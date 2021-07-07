import pandas as pd
import numpy as np

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
    # replace -999 with 0
    air = air.replace(to_replace=-999, value=0)
    # set to date time format
    air.DateTime = pd.to_datetime(air.DateTime)
    # rename features
    air = air.rename(columns={"DateTime": "datetime",
                              "AlertTriggered":"alert_triggered"})
    # return new df
    return air
#-----------------------------------------------------------------------------

# Flood Cleaning

def clean_flood():
    '''Drops unneeded columns from the med center flooding df
    Makes sure DateTime is in DateTime format'''
    # read csv
    flood = pd.read_csv('med_center_flood.csv')
    # drop the colums
    flood = flood.drop(columns=['LAT', 'LONG', 'Zone', 
                          'Sensor_id', 'SensorModel', 
                          'SensorStatus', 'AlertTriggered', 
                          'Temp_C', 'Temp_F', 'Vendor'])
    # Set to date time format
    flood.DateTime = pd.to_datetime(flood.DateTime)
    flood = flood.rename(columns={"DateTime": "datetime", 
                        "DistToWL_ft": "water_level_feet", 
                        "DistToWL_m": "water_level_meters", 
                        "DistToDF_ft": "flood_width_feet",
                        "DistToDF_m": "flood_width_meters"})
    # return new df
    return flood

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

#-----------------------------------------------------------------------------

# Split the Data into Tain, Test, and Validate.
def split_game_sales(df):
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
