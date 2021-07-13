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
    
    air['AQI_pm2_5'] = pd.cut(air.Pm2_5, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
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
    
    air['AQI_pm10'] = pd.cut(air.Pm10, 
                                bins = [-1,55,154,255,355,425,4000],
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
                        "DistToWL_ft": "sensor_to_water_feet", 
                        "DistToWL_m": "sensor_to_water_meters", 
                        "DistToDF_ft": "sensor_to_ground_feet",
                        "DistToDF_m": "sensor_to_ground_meters"})
    # create new features for flood depth
    flood['flood_depth_feet'] = flood.sensor_to_ground_feet - flood.sensor_to_water_feet
    flood['flood_depth_meters'] = flood.sensor_to_ground_meters - flood.sensor_to_water_meters
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
    sa_weather = pd.read_csv('SA_weather.csv')
    # concat sa date and time
    sa_weather['Date_Time'] = sa_weather['Date'] + ' ' + sa_weather['Time']
    # put into date time format
    sa_weather.Date_Time = pd.to_datetime(sa_weather.Date_Time)
    # round to nearest hour
    sa_weather['DateTime'] = sa_weather['Date_Time'].dt.round('60min')
    # set sa weather index
    sa_weather = sa_weather.set_index('DateTime')
    # drop old datetime
    sa_weather = sa_weather.drop(columns=['Date_Time', 'Temp', 'Humidity', 'Barometer'])
    # rename
    sa_weather = sa_weather.rename(columns={"Time": "time", 
                            "Date": "date", 
                            "Weather": "weather", 
                            "Wind": "wind",
                            "Visibility": "visibility"})
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
    #rename columns to be more readable
    weather = weather.rename(columns={"DateTime": "datetime", 
                            "Temp_C": "celsius", 
                            "Temp_F": "farenheit", 
                            "Humidity": "humidity",
                            "DewPoint_C": "dewpoint_celsius",
                            "DewPoint_F": "dewpoint_farenheit",
                            "Pressure_Pa": "pressure"})
    #change datetime to pandas datetime object
    weather.datetime = pd.to_datetime(weather.datetime)
    # round to hour
    weather['DateTime'] = weather['datetime'].dt.round('60min')
    # set index
    weather = weather.set_index('DateTime')
    # join the 2 df's
    weather = weather.join(sa_weather, how='right')
    # repalce -999
    weather = weather.replace(to_replace=-999, value=0)
    # drop nulls
    weather.dropna(inplace = True)
    #return clean weather df
    return weather

#-----------------------------------------------------------------------------

# Wrangle SAWS
def wrangle_saws():
    '''This function will drop unnecessary columns, 
    create a 'location' using data acquired from 
    other columns, and melt the data to make month year column'''
    # Reads the csv
    saws = pd.read_csv('med_center_saws.csv')
    # Removes NaN values from 'Prefix' and 'Suffix' column for concatenation in 'location'
    saws['Prefix'] = saws.Prefix.fillna(value = '')
    saws['Suffix'] = saws.Suffix.fillna(value = '')
    # Concatenating columns together for specific location
    saws['location'] = saws['Prefix'] + ' ' + saws['Service Location'] + ' ' + saws['Suffix']
    # Stripping any extra whitespace
    saws['location'] = saws.location.str.strip()
    saws = saws.drop(columns=['Unnamed: 0', 'Prefix', 'Suffix', 'Service Location'])
    saws = saws.melt(id_vars=['Record #', 'ZIP Code', 'location'], 
              var_name='Month & Year', value_name='Gallons Consumed')
    saws = saws.set_index('Record #')
    saws = saws.fillna(0)
    saws = saws.rename(columns={"ZIP Code": "zipcode", 'Month & Year':'year_month', 
                                'Gallons Consumed':'gallons_consumed'})
    return saws


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

# Daily averages and more for all COSA sataframes

def full_daily_COSA_dataframe():
    
    '''
    This function takes in all COSA dataframes,
    averages them by day, then joins them all together
    using the day as a primary key
    '''

    # Pulls sound CSV and sets datetime as index, then orders it
    sound_df = wrangle_sound()
    sound_df = sound_df.set_index('DateTime')
    sound_df = sound_df.sort_index()
    # Pulls flood CSV and sets datetime as index
    flood_df = clean_flood()
    flood_df = flood_df.set_index('datetime')
    # Pulls weather CSV
    weather_df = wrangle_weather()
    # Pulls air CSV, sets datetime column to datetime object, sets it as an index, then sorts it
    air_df = clean_air()
    air_df.datetime = pd.to_datetime(air_df.datetime)
    air_df = air_df.set_index('datetime')
    air_df = air_df.sort_index()
    # Resamples each dataframe by the day using mean, and drops unnecessary columns from air_df
    weather_day_df = weather_df.resample('D', on='datetime').mean()
    flood_day_df = flood_df.resample('D').mean()
    sound_day_df = sound_df.resample('D').mean()
    air_day_df = air_df.resample('D').mean().drop(columns = ['hour', 'weekday', 'CO_24hr', 'Pm_25_24hr', 'Pm_10_24hr', 'SO2', 'O3', 'NO2'])
    # Creating series for each pollutant
    air2_5 = air_df.drop(air_df.columns.difference(['Pm2_5', 'AQI_pm2_5']), 1)
    air10 = air_df.drop(air_df.columns.difference(['Pm10', 'AQI_pm10']), 1)
    airCO = air_df.drop(air_df.columns.difference(['CO', 'AQI_CO']), 1)
    # Pull most hazardous levels of pollution for each day
    series2_5 = air2_5.resample('D').max().rename(columns = {'AQI_pm2_5': 'most_hazardous_pm2.5_level'})['most_hazardous_pm2.5_level']
    series10 = air10.resample('D').max().rename(columns = {'AQI_pm10': 'most_hazardous_pm10_level'})['most_hazardous_pm10_level']
    seriesCO = airCO.resample('D').max().rename(columns = {'AQI_CO': 'most_hazardous_CO_level'})['most_hazardous_CO_level']
    # Joins the series together in a dataframe
    hazards = pd.DataFrame(series2_5).join(series10).join(seriesCO)
    # Joins the resampled dataframes together
    df = weather_day_df.join(air_day_df).join(hazards).join(sound_day_df).join(flood_day_df)
    # Rounds numbers in specific columns
    df = df.round({'celsius': 2, 'farenheit': 2, 'humidity': 2, 'dewpoint_celsius': 2, 'dewpoint_farenheit': 2,
          'pressure': 2, 'NoiseLevel_db': 2, 'sensor_to_water_feet': 2, 'sensor_to_water_meters': 2,
          'sensor_to_ground_feet': 2, 'sensor_to_ground_meters': 2, 'flood_depth_feet': 2,
          'flood_depth_meters': 2})
    return df