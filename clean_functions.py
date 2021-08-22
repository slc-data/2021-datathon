
# Streamlit CLEAN COSA DATA APP for Datathon
####################################################################
#COSA CSV REFERENCES 8/18/2021
# Brooks air quality:  81661d35-a5c5-40d1-af16-92edd3946579.csv
# Brooks flood:  c0c546cd-fbfa-479c-b1ca-ac7a7244aa53.csv
# Brooks sound:  3cc6c00e-0874-423f-ac81-de6081c1b532.csv
# Brooks weather:  4dc78055-6ca6-4ce8-8a36-4c22804f6a9b.csv
# Downtown air quality:  12ebf68f-95b0-4d96-9a1b-9c4f4e25497e.csv
# Downtown flood:  346d33b7-0b74-4b92-aa22-452456954ed1.csv
# Downtown sound:  f21099d0-22d7-43e7-bf06-3dac304b6765.csv
# Downton weather:  f6038372-b38f-42bb-8cf5-5d6419a46cf1.csv
# Med center air quality:  0f16d9bc-fdf4-45fb-8198-dab84dc67ad7.csv
# med center flood:  aaf0e6a5-8df7-4f0c-bf22-7b2f6ad6943d.csv
# med center sound:  31f8a3f4-bc73-48c4-96bf-768388129f85.csv
# med center weather:  7c2649a6-bb5a-4579-ab86-fbaee4e7024a.csv  
#####################################################################
# Imports
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import streamlit.components as stc

# Flood Cleaning
def clean_flood(df):
    '''Drops unneeded columns from the med center flooding df
    Makes sure DateTime is in DateTime format'''
    # drop the columns
    df = df.drop(columns=['Temp_C', 'Temp_F', 'DistToDF_m', 'DistToWL_m'])
    # Set to date time format
    df.DateTime = pd.to_datetime(df.DateTime)
    df = df.rename(columns={
        "DateTime": "datetime",
        "Sensor_id": "sensor_id",
        "Vendor": "vendor",
        "SensorModel": "sensor_model",
        "LAT": "latitude",
        "LONG": "longitude",
        "Zone": "pilot_zone",
        "DistToWL_ft": "sensor_to_water_feet",
        "DistToDF_ft": "sensor_to_ground_feet",
        "AlertTriggered": "alert_triggered",
        "SensorStatus": "sensor_status"})
    # replace -999 with 0
    df["sensor_to_ground_feet"].replace({-999:13.5006561680}, inplace=True)

    
    #flood = flood.replace(to_replace=-999, value=0)
    # create new features for flood depth
    df['flood_depth_feet'] = df.sensor_to_ground_feet - df.sensor_to_water_feet

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
    df['flood_alert'] = df.apply(flood_alert, axis=1)
    df = df[(df.sensor_to_water_feet != -999)]
    # return new df
    return df

# Air cleaning
#-----------------------------------------------------------------------------

# Air Quality Cleaning
def clean_air(df):
    '''Drops unneeded columns from the air quality df
    then handles the nulls in alert triggered column
    set to date time format'''
    # drop the colums
    df = df.drop(columns=['LAT', 'LONG', 'SensorStatus'])
    # replace nulls in ALertTriggered to None
    df.fillna("None", inplace = True)
    # set to date time format
    df.DateTime = pd.to_datetime(df.DateTime)
    # rename features
    df = df.rename(columns={"DateTime": "datetime",
                              "AlertTriggered": "alert_triggered",
                              "Sensor_id": "sensor_id",
                              "Vendor": "vendor",
                              "SensorModel": "sensor_model"})
    df = df.replace(to_replace=-999, value=0)
    # create time series features
    df['dates'] = pd.to_datetime(df['datetime']).dt.date
    df['time'] = pd.to_datetime(df['datetime']).dt.time
    df['hour'] = pd.to_datetime(df['datetime']).dt.hour
    df['weekday'] = pd.to_datetime(df['datetime']).dt.weekday
    # make all CO bins
    df['AQI_CO'] = pd.cut(df.CO, 
                            bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                            labels = ['Good', 'Moderate', 
                                      'Unhealthy for Sensitive Groups', "Unhealthy", 
                                      "Very Unhealthy", 'Hazardous'])
    
    CO_24hr = df.groupby('dates', as_index=False)['CO'].mean()
    CO_24hr = CO_24hr.rename(columns={'CO':'CO_24hr'})
    df = df.merge(CO_24hr, on = 'dates', how ='left')
    df['AQI_CO_24hr'] = pd.cut(df.CO_24hr, 
                                bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    
    df['AQI_pm2_5'] = pd.cut(df.Pm2_5, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    pm_25_24hr = df.groupby('dates', as_index=False)['Pm2_5'].mean()
    pm_25_24hr = pm_25_24hr.rename(columns={'Pm2_5':'Pm_25_24hr'})
    df = df.merge(pm_25_24hr, on = 'dates', how ='left')
    df['AQI_pm_25_24hr'] = pd.cut(df.Pm_25_24hr, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    
    df['AQI_pm10'] = pd.cut(df.Pm10, 
                                bins = [-1,55,154,255,355,425,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    pm_10_24hr = df.groupby('dates', as_index=False)['Pm10'].mean()
    pm_10_24hr = pm_10_24hr.rename(columns={'Pm10':'Pm_10_24hr'})
    df = df.merge(pm_10_24hr, on = 'dates', how ='left')
    df['AQI_pm10_24hr'] = pd.cut(df.Pm_10_24hr, 
                                bins = [-1,55,154,255,355,425,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # create new unhealthy alert system
    def df_alert(c):
        if c['Pm2_5'] > 55.4:
            return 'Pm2_5'
        elif c['Pm10'] > 254.9:
            return 'Pm10'
        elif c['CO'] > 12.4:
            return 'CO'
        else:
            return 'No Alert'
    df['unhealthy_alert'] = df.apply(df_alert, axis=1)
    # create new sensitive alert system
    def sensitive_df_alert(c):
        if c['Pm2_5'] > 34.4:
            return 'Pm2_5'
        elif c['Pm10'] > 154.9:
            return 'Pm10'
        elif c['CO'] > 9.4:
            return 'CO'
        else:
            return 'No Alert'
    df['sensitive_alert'] = df.apply(sensitive_df_alert, axis=1)
    # create unhealthy HYPOTHTICAL Alert system
        # hypothetical alerts are based on IF everything is reading in PPM
    def hypo_df_alert(c):
        if c['Pm2_5'] > 55.4:
            return 'Pm2_5'
        elif c['Pm10'] > 254.9:
            return 'Pm10'
        elif c['CO'] > 12.4:
            return 'CO'
        elif c['SO2'] > 0.1859:
            return 'SO2'
        elif c['O3'] > 0.1649:
            return 'O3'
        elif c['NO2'] > 0.3609:
            return 'NO2'
        else:
            return 'No Alert'
    df['hypothetical_unhealthy_alert'] = df.apply(hypo_df_alert, axis=1)
    # create sensitive HYPOTHTICAL Alert system
        # hypothetical alerts are based on IF everything is reading in PPM
    def sensitive_df_alert(c):
        if c['Pm2_5'] > 34.4:
            return 'Pm2_5'
        elif c['Pm10'] > 154.9:
            return 'Pm10'
        elif c['CO'] > 9.4:
            return 'CO'
        elif c['SO2'] > 0.0759:
            return 'SO2'
        elif c['O3'] > 0.124:
            return 'O3'
        elif c['NO2'] > 0.1009:
            return 'NO2'
        else:
            return 'No Alert'

    df['hypothetical_sensitive_alert'] = df.apply(sensitive_df_alert, axis=1)
    # return new df
    return df

#-----------------------------------------------------------------------------
# Sound Cleaning
def wrangle_sound(df):
    '''
    This function drops unnecessary columns and
    converts the 'DateTime' column to a datetime 
    object
    '''
    # Drops unnecessary columns
    df = df.drop(columns = ['SensorStatus', 'LONG', 'LAT'])
    # Converts to datetime
    df['DateTime'] = pd.to_datetime(df.DateTime)
    # make noise level feature
    df['how_loud'] = pd.cut(df.NoiseLevel_db, 
                                bins = [-1,46,66,81,101,4000],
                                labels = ['Normal', 'Moderate', 
                                          'Loud', "Very Loud", 
                                          "Extremely Loud"])
    df = df.rename(columns={"DateTime": "datetime",
                              "AlertTriggered": "alert_triggered",
                              "Sensor_id": "sensor_id",
                              "Vendor": "vendor",
                              "SensorModel": "sensor_model"})
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

# Weather Cleaning

def wrangle_weather(df):
    '''
    This function will drop unneccessary columns, 
    change datetime to a pandas datetime datatype,
    and rename columns to be more readable to return
    a clean dataframe.  
    '''
    #change datetime to pandas datetime object
    df.DateTime = pd.to_datetime(df.DateTime)
    # round to hour
    df['DateTime'] = df['DateTime'].dt.round('60min')
    # set index
    df = df.set_index('DateTime')
    # drop old columns
    df = df.drop(columns=['Temp_C', 'DewPoint_C', 'SensorStatus'])
    # rename
    df = df.rename(columns={
                            "DateTime": "datetime", 
                            "Sensor_id": "sensor_id" 
                            "LAT": "latitude",
                            "LONG": "longitude",
                            "SensorModel": "sensor_model",
                            "Vendor": "vendor",
                            "Zone": "pilot_zone",
                            "DewPoint_F": "dewpoint_f",
                            "Pressure_Pa": "pressure_pa"})

    # repalce -999
    df = df.replace(to_replace=-999, value=0)
    # drop nulls
    df.dropna(inplace = True)
    return df