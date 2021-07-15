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

# For the following 3 recommendations we rolled up the data for a 24 hour time range average.
    # So if you plan to use any of these 3 makes sure to use this function as well
def create_dates(df):
    '''creates column to hold only the date'''
    # datetime format
    df.DateTime = pd.to_datetime(df.DateTime)
    # replace -999 with 0
    df = df.replace(to_replace=-999, value=0)
    # create new column
    df['dates'] = pd.to_datetime(df['DateTime']).dt.date
    return df

#-----------------------------------------------------------------------------

# Adding in air qulity index for Carbon Monoxide
    # note that AQI for carbon monoxide is usually read in 8 hour incriments.
    # but we used it in individual readings and in 24 hour incriments.
def add_individual_pm2_5_AQI(df):
    '''This AQI will read each idividual reading for pm 2.5'''
    # create aqi for each reading of CO
    df['AQI_CO'] = pd.cut(df.CO, 
                        bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                        labels = ['Good', 'Moderate', 
                                  'Unhealthy for Sensitive Groups', "Unhealthy", 
                                  "Very Unhealthy", 'Hazardous'])
    # return df with AQI
    return df

def add_daily_CO_AQI(df):
    '''This AQI will read the dates column
            (must run the create_dates funciton first)
       and create the daily average AQI'''
    # create the daily average
    CO_24hr = df.groupby('dates', as_index=False)['CO'].mean()
    CO_24hr = CO_24hr.rename(columns={'CO':'CO_daily'})
    df = df.merge(CO_24hr, on = 'dates', how ='left')
    df['daily_CO_AQI'] = pd.cut(df.CO_daily, 
                                bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    return df

#-----------------------------------------------------------------------------

# Adding in air qulity index for PM 2.5
    # note that AQI for this is usually read in 24 hour incriments.
    # but we used it in individual readings and in 24 hour incriments.
def add_individual_pm2_5_AQI(df):
    '''This AQI will read each idividual reading for pm 2.5'''
    # create aqi for each reading of Pm2_5
    df['AQI_pm2_5'] = pd.cut(df.Pm2_5, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # return df with AQI
    return df

def add_daily_pm2_5_AQI(df):
    '''This AQI will read the dates column
            (must run the create_dates funciton first)
       and create the daily average AQI'''
    # create the daily average
    pm_25_24hr = df.groupby('dates', as_index=False)['Pm2_5'].mean()
    pm_25_24hr = pm_25_24hr.rename(columns={'Pm2_5':'daily_pm2_5'})
    df = df.merge(pm_25_24hr, on = 'dates', how ='left')
    df['daily_pm2_5_AQI'] = pd.cut(df.daily_pm2_5, 
                                bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    return df
    
#-----------------------------------------------------------------------------

# Adding in air qulity index for PM 10
    # note that AQI for this is usually read in 24 hour incriments.
    # but we used it in individual readings and in 24 hour incriments.
def add_individual_pm10_AQI(df):
    '''This AQI will read each idividual reading for pm 2.5'''
    # create aqi for each reading of Pm2_5
    df['AQI_pm10'] = pd.cut(df.Pm10, 
                            bins = [-1,55,154,255,355,425,4000],
                            labels = ['Good', 'Moderate', 
                                      'Unhealthy for Sensitive Groups', "Unhealthy", 
                                      "Very Unhealthy", 'Hazardous'])
    # return df with AQI
    return df
    
def add_daily_pm10_AQI(df):
    '''This AQI will read the dates column
            (must run the create_dates funciton first)
       and create the daily average AQI'''
    # create the daily average
    pm_10_24hr = df.groupby('dates', as_index=False)['Pm10'].mean()
    pm_10_24hr = pm_10_24hr.rename(columns={'Pm10':'Pm_10_daily'})
    df = df.merge(pm_10_24hr, on = 'dates', how ='left')
    df['daily_pm10_AQI'] = pd.cut(df.Pm_10_24hr, 
                                bins = [-1,55,154,255,355,425,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    return df


#-----------------------------------------------------------------------------

# Reconfigure air quality alerts
    # Note that the following code(s) are hypothetical if everything is being read in the way the data dictionary states:
        # Pm2_5 being read in (Microgram per meter cube)
        # Pm10 being read in (Microgram per meter cube)
        # CO being read in (PPM)
        # O3 being read in (PPM)
        # SO2 being read in (PPM)
        # NO2 being rad in (PPM)
    # This means that O3, SO2, and NO2 will have a lot of bed readings (we think that these 3 are actually being read in ppb, if this is true you may need to convert these numbers to ppb or change the sensors reading to be ppm)
    
def add_unhealthy_alert(df):
    '''THis causes an alert to trigger for the readings that are:
    unhealthy, very unhealthy, or hazerdoes'''
    def unhealthy_air_alert(c):
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
    df['unhealthy_alert'] = df.apply(unhealthy_air_alert, axis=1)
    return df

def add_sensitive_alert(df):
    '''THis causes an alert to trigger for the readings that are:
    unhealthy for sensitive groups, unhealthy, very unhealthy, or hazerdoes'''
    def sensitive_air_alert(c):
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
    df['sensitive_alert'] = df.apply(sensitive_air_alert, axis=1)
    return df

#-----------------------------------------------------------------------------

# Re-configure sound alert
    # We decided to alert to minor and major risks over time
        # over 80 decibles will trigger a minor risk because over time80 db will cause minor damage
        # over 120 triggers as major risk because over time will cause major damage.
def add_sound_alert(df):
    '''Creates an alert if sound level gets to be over 80 and 120'''
    # create parameters
    def sound_alert(c):
        if c['NoiseLevel_db'] > 80:
            return 'Minor Risk'
        elif c['NoiseLevel_db'] > 120:
            return 'Major Risk'
        else:
            return 'No Alert'
        # apply to df
    df['sound_alert'] = df.apply(sound_alert, axis=1)
    return df

# Add in noise level in laymen's terms
def add_laymens_terms(df):
    '''says if the noise level is 
    normal, moderate, loud, very loud, or extremelt loud'''
    # make noise level feature
    df['noise_level'] = pd.cut(df.NoiseLevel_db, 
                                bins = [-1,46,66,81,101,4000],
                                labels = ['Normal', 'Moderate', 
                                          'Loud', "Very Loud", 
                                          "Extremely Loud"])
    return df