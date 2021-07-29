import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# turn off pink warning boxes
import warnings
warnings.filterwarnings("ignore")


#-----------------------------------------------------------------------------

def clean_flood(flood):
    '''Drops unneeded columns from the med center flooding df
    Makes sure DateTime is in DateTime format'''
    # drop the columns
    flood = flood.drop(columns=['LAT', 'LONG', 'Zone',  
                          'SensorStatus', 'AlertTriggered', 
                          'Temp_C', 'Temp_F', 'Vendor'])
    # Set to date time format
    flood.DateTime = pd.to_datetime(flood.DateTime)
    flood = flood.rename(columns={"DateTime": "datetime", 
                        "DistToWL_ft": "sensor_to_water_feet", 
                        "DistToWL_m": "sensor_to_water_meters", 
                        "DistToDF_ft": "sensor_to_ground_feet",
                        "DistToDF_m": "sensor_to_ground_meters"})
    # replae -999 with 0
    flood["sensor_to_ground_feet"].replace({-999:13.5006561680}, inplace=True)
    flood["sensor_to_ground_meters"].replace({-999:4.115}, inplace=True)
    
    #flood = flood.replace(to_replace=-999, value=0)
    # create new features for flood depth
    flood['flood_depth_feet'] = flood.sensor_to_ground_feet - flood.sensor_to_water_feet
    flood['flood_depth_meters'] = flood.sensor_to_ground_meters - flood.sensor_to_water_meters 
    # Create new alert
    def flood_alert(c):
        if 0 < c['flood_depth_feet'] < 0.66667:
            return 'No Risk'
        elif 0.66667 < c['flood_depth_feet'] < 1.08333:
            return 'Minor Risk'
        elif 1.08333 < c['flood_depth_feet'] < 2.16667:
            return 'Moderate Risk'
        elif 2.16667 < c['flood_depth_feet']:
            return 'Major Risk !'
        else:
            return 'No Alert'
    flood['flood_alert'] = flood.apply(flood_alert, axis=1)
    flood = flood[(flood.sensor_to_water_feet != -999)]
    # return new df
    return flood

#-----------------------------------------------------------------------------
def clean_air(air):
    '''Drops unneeded columns from the air quality df
    then handles the nulls in alert triggered column
    set to date time format'''
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
    return air
#-----------------------------------------------------------------------------
def wrangle_weather(weather):
    '''
    This function will drop unneccessary columns, 
    change datetime to a pandas datetime datatype,
    and rename columns to be more readable to return
    a clean dataframe.  
    '''
    #read csv and turn into pandas dataframe
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
def wrangle_sound(df):
    '''
    This function drops unnecessary columns and
    converts the 'DateTime' column to a datetime 
    object
    '''

    # Drops unnecessary columns
    df = df.drop(columns = ['SensorStatus', 'AlertTriggered', 'Zone', 'LONG', 
                            'LAT', 'SensorModel', 'Vendor', 'Sensor_id'])
    # Converts to datetime
    df['DateTime'] = pd.to_datetime(df.DateTime)
    # make noise level feature
    df['how_loud'] = pd.cut(df.NoiseLevel_db, 
                                bins = [-1,46,66,81,101,4000],
                                labels = ['Normal', 'Moderate', 
                                          'Loud', "Very Loud", 
                                          "Extremely Loud"])
    def sound_alert(c):
        if c['NoiseLevel_db'] > 80:
            return 'Minor Risk'
        elif c['NoiseLevel_db'] > 120:
            return 'Major Risk'
        else:
            return 'No Alert'
    df['sound_alert'] = df.apply(sound_alert, axis=1)
    return df
#-----------------------------------------------------------------------------

def full_daily_downtown_COSA_dataframe():
    
    '''
    This function takes in all COSA dataframes,
    averages them by day, then joins them all together
    using the day as a primary key
    '''

    # Pulls sound CSV and sets datetime as index, then orders it
    df = pd.read_csv('downtown_sound.csv')
    sound_df = wrangle_sound(df)
    sound_df = sound_df.set_index('DateTime')
    sound_df = sound_df.sort_index()
    # Pulls flood CSV and sets datetime as index
    flood = pd.read_csv('downtown_flood.csv')
    flood_df = clean_flood(flood)
    flood_df = flood_df.set_index('datetime')
    # Pulls weather CSV
    weather = pd.read_csv('downtown_weather.csv')
    weather_df = wrangle_weather(weather)
    # Pulls air CSV, sets datetime column to datetime object, sets it as an index, then sorts it
    air = pd.read_csv('downtown_air.csv')
    air_df = clean_air(air)
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
    # Create AQI for CO
    df['AQI_CO'] = pd.cut(df.CO, 
                            bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                            labels = ['Good', 'Moderate', 
                                      'Unhealthy for Sensitive Groups', "Unhealthy", 
                                      "Very Unhealthy", 'Hazardous'])
    # create AQi for pm 2.5
    df['AQI_pm2_5'] = pd.cut(df.Pm2_5, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # create AQI for pm 10
    df['AQI_pm10'] = pd.cut(df.Pm10, 
                                bins = [-1,55,154,255,355,425,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    return df

#-----------------------------------------------------------------------------

def full_daily_medcenter_COSA_dataframe():
    
    '''
    This function takes in all COSA dataframes,
    averages them by day, then joins them all together
    using the day as a primary key
    '''

    # Pulls sound CSV and sets datetime as index, then orders it
    df = pd.read_csv('med_center_sound.csv')
    sound_df = wrangle_sound(df)
    sound_df = sound_df.set_index('DateTime')
    sound_df = sound_df.sort_index()
    # Pulls flood CSV and sets datetime as index
    flood = pd.read_csv('med_center_flood.csv')
    flood_df = clean_flood(flood)
    flood_df = flood_df.set_index('datetime')
    # Pulls weather CSV
    weather = pd.read_csv('med_center_weather.csv')
    weather_df = wrangle_weather(weather)
    # Pulls air CSV, sets datetime column to datetime object, sets it as an index, then sorts it
    air = pd.read_csv('med_center_air.csv')
    air_df = clean_air(air)
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
    # Create AQI for CO
    df['AQI_CO'] = pd.cut(df.CO, 
                            bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                            labels = ['Good', 'Moderate', 
                                      'Unhealthy for Sensitive Groups', "Unhealthy", 
                                      "Very Unhealthy", 'Hazardous'])
    # create AQi for pm 2.5
    df['AQI_pm2_5'] = pd.cut(df.Pm2_5, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # create AQI for pm 10
    df['AQI_pm10'] = pd.cut(df.Pm10, 
                                bins = [-1,55,154,255,355,425,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    return df

#-----------------------------------------------------------------------------

def full_daily_brooks_COSA_dataframe():
    
    '''
    This function takes in all COSA dataframes,
    averages them by day, then joins them all together
    using the day as a primary key
    '''

    # Pulls sound CSV and sets datetime as index, then orders it
    df = pd.read_csv('brooks_sound.csv')
    sound_df = wrangle_sound(df)
    sound_df = sound_df.set_index('DateTime')
    sound_df = sound_df.sort_index()
    # Pulls flood CSV and sets datetime as index
    flood = pd.read_csv('brooks_flood.csv')
    flood_df = clean_flood(flood)
    flood_df = flood_df.set_index('datetime')
    # Pulls weather CSV
    weather = pd.read_csv('brooks_weather.csv')
    weather_df = wrangle_weather(weather)
    # Pulls air CSV, sets datetime column to datetime object, sets it as an index, then sorts it
    air = pd.read_csv('brooks_air.csv')
    air_df = clean_air(air)
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
    # Create AQI for CO
    df['AQI_CO'] = pd.cut(df.CO, 
                            bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                            labels = ['Good', 'Moderate', 
                                      'Unhealthy for Sensitive Groups', "Unhealthy", 
                                      "Very Unhealthy", 'Hazardous'])
    # create AQi for pm 2.5
    df['AQI_pm2_5'] = pd.cut(df.Pm2_5, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # create AQI for pm 10
    df['AQI_pm10'] = pd.cut(df.Pm10, 
                                bins = [-1,55,154,255,355,425,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    return df