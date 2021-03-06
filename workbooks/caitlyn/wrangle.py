import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# turn off pink warning boxes
import warnings
warnings.filterwarnings("ignore")

import sklearn

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
#-----------------------------------------------------------------------------
def full_air_df():
    '''Combines air quality dataframes for:
        brooks
        downtown
        medical center
    into one main df.'''
    # read medical center and clean it
    med_air = pd.read_csv('med_center_air.csv')
    med_air = wrangle.clean_air(med_air)
    # read downtown and clean it
    down_air = pd.read_csv('downtown_air.csv')
    down_air = wrangle.clean_air(down_air)
    #read the brooks and clean it
    brooks_air = pd.read_csv('brooks_air.csv')
    brooks_air = wrangle.clean_air(brooks_air)
    # specify what df's to combine together
    frames = [med_air, down_air, brooks_air]
    # concat the df's together
    df = pd.concat(frames)
    return df
#-----------------------------------------------------------------------------
def full_flood_df():
    '''Combines flood dataframes for:
        brooks
        downtown
        medical center
    into one main df.'''
    # read medical center and clean it
    med_flood = pd.read_csv('med_center_flood.csv')
    med_flood = wrangle.clean_flood(med_flood)
    # read downtown and clean it
    down_flood = pd.read_csv('downtown_flood.csv')
    down_flood = wrangle.clean_flood(down_flood)
    #read the brooks and clean it
    brooks_flood = pd.read_csv('brooks_flood.csv')
    brooks_flood = wrangle.clean_flood(brooks_flood)
    # specify what df's to combine together
    frames = [med_flood, down_flood, brooks_flood]
    # concat the df's together
    df = pd.concat(frames)
    return df

#-----------------------------------------------------------------------------
def full_sound_df():
    '''Combines sound dataframes for:
        brooks
        downtown
        medical center
    into one main df.'''
    # read medical center and clean it
    med_sound = pd.read_csv('med_center_sound.csv')
    med_sound = wrangle.wrangle_sound(med_sound)
    # read downtown and clean it
    down_sound = pd.read_csv('downtown_sound.csv')
    down_sound = wrangle.wrangle_sound(down_sound)
    #read the brooks and clean it
    brooks_sound = pd.read_csv('brooks_sound.csv')
    brooks_sound = wrangle.wrangle_sound(brooks_sound)
    # specify what df's to combine together
    frames = [med_sound, down_sound, brooks_sound]
    # concat the df's together
    df = pd.concat(frames)
    return df

#-----------------------------------------------------------------------------
def full_weather_df():
    '''Combines weather dataframes for:
        brooks
        downtown
        medical center
    into one main df.'''
    # read medical center and clean it
    med_weather = pd.read_csv('med_center_weather.csv')
    med_weather = wrangle.wrangle_weather(med_weather)
    # read downtown and clean it
    down_weather = pd.read_csv('downtown_weather.csv')
    down_weather = wrangle.wrangle_weather(down_weather)
    #read the brooks and clean it
    brooks_weather = pd.read_csv('brooks_weather.csv')
    brooks_weather = wrangle.wrangle_weather(brooks_weather)
    # specify what df's to combine together
    frames = [med_weather, down_weather, brooks_weather]
    # concat the df's together
    df = pd.concat(frames)
    return df

#-----------------------------------------------------------------------------

# Air Quality Cleaning
def clean_air(df):
    '''Drops unneeded columns from the air quality df
    then handles the nulls in alert triggered column
    set to date time format'''
    # drop the colums
    df = df.drop(columns=['LAT', 'LONG',
                            'Sensor_id', 'SensorModel', 
                            'SensorStatus', 'Vendor'])
    # replace nulls in ALertTriggered to None
    df.fillna("None", inplace = True)
    # set to date time format
    df.DateTime = pd.to_datetime(df.DateTime)
    # rename features
    df = df.rename(columns={"DateTime": "datetime",
                              "AlertTriggered":"alert_triggered"})
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

# Flood Cleaning

# Flood Cleaning
def clean_flood(df):
    '''Drops unneeded columns from the med center flooding df
    Makes sure DateTime is in DateTime format'''
    # drop the columns
    df = df.drop(columns=['LAT', 'LONG',  
                          'SensorStatus', 'AlertTriggered', 
                          'Temp_C', 'Temp_F', 'Vendor'])
    # Set to date time format
    df.DateTime = pd.to_datetime(df.DateTime)
    df = df.rename(columns={"DateTime": "datetime", 
                        "DistToWL_ft": "sensor_to_water_feet", 
                        "DistToWL_m": "sensor_to_water_meters", 
                        "DistToDF_ft": "sensor_to_ground_feet",
                        "DistToDF_m": "sensor_to_ground_meters"})
    # replae -999 with 0
    df["sensor_to_ground_feet"].replace({-999:13.5006561680}, inplace=True)
    df["sensor_to_ground_meters"].replace({-999:4.115}, inplace=True)
    
    #flood = flood.replace(to_replace=-999, value=0)
    # create new features for flood depth
    df['flood_depth_feet'] = df.sensor_to_ground_feet - df.sensor_to_water_feet
    df['flood_depth_meters'] = df.sensor_to_ground_meters - df.sensor_to_water_meters 
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

#-----------------------------------------------------------------------------

# Weather Cleaning
def wrangle_weather(df):
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
    df.drop(columns=[
    'Sensor_id', 
    'Vendor', 
    'SensorModel', 
    'LAT', 
    'LONG', 
    'AlertTriggered', 
    'SensorStatus'], inplace=True)
    #rename columns to be more readable
    df = df.rename(columns={"DateTime": "datetime", 
                            "Temp_C": "celsius", 
                            "Temp_F": "farenheit", 
                            "Humidity": "humidity",
                            "DewPoint_C": "dewpoint_celsius",
                            "DewPoint_F": "dewpoint_farenheit",
                            "Pressure_Pa": "pressure"})
    #change datetime to pandas datetime object
    df.datetime = pd.to_datetime(df.datetime)
    # round to hour
    df['DateTime'] = df['datetime'].dt.round('60min')
    # set index
    df = df.set_index('DateTime')
    # join the 2 df's
    df = df.join(sa_weather, how='right')
    # repalce -999
    df = df.replace(to_replace=-999, value=0)
    # drop nulls
    df.dropna(inplace = True)
    # adjust wind and visibility to be int
    df['wind'] = df.wind.replace(to_replace=" NULL",value=0)
    df['wind'] = df['wind'].str.extract('(\d+)', expand=False)
    df['visibility'] = df['visibility'].str.extract('(\d+)', expand=False)
    df["wind"].fillna(0, inplace = True)
    df['wind'] = df['wind'].astype(int)
    df['visibility'] = df['visibility'].astype(int)
    #return clean weather df
    return df

#-----------------------------------------------------------------------------

# Wrangle SAWS

def fix_dates(saws):
    '''
    Function to fix year month column into
    datetime.  Adds arbitraty day. but keeps 
    the same month and year.  
    '''
    saws['datetime'] = '01-20' + saws['year_month']
    saws.datetime = pd.to_datetime(saws.datetime)
    return saws

def wrangle_saws():
    '''This function will drop unnecessary columns, 
    create a 'location' using data acquired from 
    other columns, and melt the data to make month year column'''
    # Reads the med center csv
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
    return fix_dates(saws)
    
    
#-----------------------------------------------------------------------------

# Sound Cleaning
def wrangle_sound(df):
    '''
    This function drops unnecessary columns and
    converts the 'DateTime' column to a datetime 
    object
    '''
    # Drops unnecessary columns
    df = df.drop(columns = ['SensorStatus', 'AlertTriggered', 'LONG', 
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

def show_saws():

    '''
    This function plots the SAWS dataset
    by both streets and dates
    '''
    
    # Pulls the data
    saws_df = wrangle_saws()
    # Creates a new column that has the date in a "year month" format that can be converted to a datetime object
    saws_df['year_month'] = '20' + saws_df['year_month']
    # Converts to datetime
    saws_df['year_month'] = pd.to_datetime(saws_df['year_month'])
    # Sets the index to the datetime object, then groups the data by month and drops zipcode (since they are all in the same one)
    saws_month_year = saws_df.set_index('year_month').resample('M').mean().drop(columns = ['zipcode'])
    # Creates a new column for labeling graphs with month and year
    saws_month_year['Date'] = pd.to_datetime(saws_month_year.index)
    # Truncates the 'Date' column into just month and year
    saws_month_year['Mon_Year'] = saws_month_year['Date'].dt.strftime('%b-%Y')
    # Creates a new dataframe for the mean of gallons used by street
    saws_places = saws_df.groupby('location').mean()
    # Drops zipcode column
    saws_places = saws_places.drop(columns =['zipcode'])
    # Creates a new dataframe for the sum of gallons used by street
    saws_places_sum = saws_df.groupby('location').sum()
    import calendar
    # Creates dataframe for repesenting months by mean monthly water usage
    saws_year_month_mean = saws_df.gallons_consumed.groupby(saws_df['year_month'].dt.month).mean()
    saws_year_month_mean = pd.DataFrame(saws_year_month_mean)
    saws_year_month_mean['month'] = saws_year_month_mean.index
    # Labels numeric months into their respective shortened titles
    saws_year_month_mean['month'] = saws_year_month_mean['month'].apply(lambda x: calendar.month_abbr[x])
    
    plt.subplots(4, 1, figsize=(24, 40), sharey=True)
    plt.subplots_adjust(hspace=.5)
    sns.set(style="darkgrid")
        
    plt.subplot(4, 1, 1)
    plt.title('Average Monthly Water Use by Street')
    plt.xticks(rotation = 90)
    sns.barplot(data = saws_places, x = saws_places.index, y = 'gallons_consumed', palette = "viridis")
    plt.xlabel('Street Name')
    plt.ylabel('Average Monthly Gallons')
    
    plt.subplot(4, 1, 2)
    plt.title('Sum of All Gallons Consumed by Street')
    plt.xticks(rotation = 90)
    sns.barplot(data = saws_places_sum, x = saws_places_sum.index, y = 'gallons_consumed', palette = "viridis")
    plt.xlabel('Street Name')
    plt.ylabel('Sum of Monthly Gallons')
    
    plt.subplot(4, 1, 3)
    plt.title('Mean Property Consumption by Month Over 4 Year Period')
    plt.xticks(rotation = 90)
    sns.barplot(data = saws_month_year, x = saws_month_year['Mon_Year'], y = 'gallons_consumed', palette = "viridis")
    plt.xlabel('Month')
    plt.ylabel('Mean Property Consumption')
    
    plt.subplot(4, 1, 4)
    plt.title('Mean Property Consumption by Month of Year')
    sns.barplot(data = saws_year_month_mean, x = 'month', y = 'gallons_consumed', palette = "viridis")
    plt.xlabel('Month')
    plt.ylabel('Mean Property Consumption')
    
#-----------------------------------------------------------------------------

# create air df based on 1 hr incriments
def air_1hr_avg(df):
    '''Takes in air df and creates every 8 hour averages'''
    # duplicate datetime column
    df['round_1hr'] = df['datetime']
    # round to every 8 hours
    df['round_1hr'] = df['round_1hr'].dt.round('60min')
    # create mew df based on the rouned time
    average_1hr = df.groupby('round_1hr', as_index=False).mean()
    # Create AQI for CO
    average_1hr['AQI_CO'] = pd.cut(average_1hr.CO, 
                                bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # Create AQI for Pm2_5
    average_1hr['AQI_pm2_5'] = pd.cut(average_1hr.Pm2_5, 
                                    bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # Create AQI for Pm10
    average_1hr['AQI_pm10'] = pd.cut(average_1hr.Pm10, 
                                    bins = [-1,55,154,255,355,425,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for SO2
    average_1hr['AQI_SO2'] = pd.cut(average_1hr.SO2, 
                                    bins = [-1,0.0359,0.0759,0.1859,0.3049,0.6049,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for NO2
    average_1hr['AQI_NO2'] = pd.cut(average_1hr.NO2, 
                                    bins = [-1,0.0539,0.1009,0.3609,0.6499,1.2499,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for O3
    average_1hr['AQI_O3'] = pd.cut(average_1hr.O3, 
                                    bins = [-1,0.06259,0.1259,0.1649,0.2049,0.4049,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # rename the new date time column
    average_1hr = average_1hr.rename(columns={"round_1hr": "datetime"})
    # Create df alerts
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
    average_1hr['unhealthy_alert'] = average_1hr.apply(unhealthy_df_alert, axis=1)
    # create sensitive HYPOTHTICAL Alert system
        # hypothetical alerts are based on IF everything is reading in PPM
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

    average_1hr['sensitive_alert'] = average_1hr.apply(sensitive_air_alert, axis=1)
    return average_1hr

#-----------------------------------------------------------------------------
# air df in 8 hour incriments
def air_8hr_avg(df):
    '''Takes in df df and creates every 8 hour averages'''
    # duplicate datetime column
    df['round_8hr'] = df['datetime']
    # round to every 8 hours
    df['round_8hr'] = df['round_8hr'].dt.round('480min')
    # create mew df based on the rouned time
    average_8hr = df.groupby('round_8hr', as_index=False).mean()
    # Create AQI for CO
    average_8hr['AQI_CO'] = pd.cut(average_8hr.CO, 
                                bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # Create AQI for Pm2_5
    average_8hr['AQI_pm2_5'] = pd.cut(average_8hr.Pm2_5, 
                                    bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # Create AQI for Pm10
    average_8hr['AQI_pm10'] = pd.cut(average_8hr.Pm10, 
                                    bins = [-1,55,154,255,355,425,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for SO2
    average_8hr['AQI_SO2'] = pd.cut(average_8hr.SO2, 
                                    bins = [-1,0.0359,0.0759,0.1859,0.3049,0.6049,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for NO2
    average_8hr['AQI_NO2'] = pd.cut(average_8hr.NO2, 
                                    bins = [-1,0.0539,0.1009,0.3609,0.6499,1.2499,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for O3
    average_8hr['AQI_O3'] = pd.cut(average_8hr.O3, 
                                    bins = [-1,0.0549,0.0709,0.0859,0.1059,0.2009,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # rename the new date time column
    average_8hr = average_8hr.rename(columns={"round_8hr": "datetime"})
    # Create df alerts
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
    # Apply alert
    average_8hr['unhealthy_alert'] = average_8hr.apply(unhealthy_df_alert, axis=1)
    # create sensitive HYPOTHTICAL Alert system
        # hypothetical alerts are based on IF everything is reading in PPM
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
    # apply alert
    average_8hr['sensitive_alert'] = average_8hr.apply(sensitive_air_alert, axis=1)
    return average_8hr

#-----------------------------------------------------------------------------

# create air df based on 12 hr incriments
def air_12hr_avg(df):
    '''Takes in df df and creates every 8 hour averages'''
    # duplicate datetime column
    df['round_12hr'] = df['datetime']
    # round to every 8 hours
    df['round_12hr'] = df['round_12hr'].dt.round('720min')
    # create mew df based on the rouned time
    average_12hr = df.groupby('round_12hr', as_index=False).mean()
    # Create AQI for CO
    average_12hr['AQI_CO'] = pd.cut(average_12hr.CO, 
                                bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # Create AQI for Pm2_5
    average_12hr['AQI_pm2_5'] = pd.cut(average_12hr.Pm2_5, 
                                    bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # Create AQI for Pm10
    average_12hr['AQI_pm10'] = pd.cut(average_12hr.Pm10, 
                                    bins = [-1,55,154,255,355,425,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for SO2
    average_12hr['AQI_SO2'] = pd.cut(average_12hr.SO2, 
                                    bins = [-1,0.0359,0.0759,0.1859,0.3049,0.6049,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for NO2
    average_12hr['AQI_NO2'] = pd.cut(average_12hr.NO2, 
                                    bins = [-1,0.0539,0.1009,0.3609,0.6499,1.2499,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for O3
    average_12hr['AQI_O3'] = pd.cut(average_12hr.O3, 
                                    bins = [-1,0.0549,0.0709,0.0859,0.1059,0.2009,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # rename the new date time column
    average_12hr = average_12hr.rename(columns={"round_12hr": "datetime"})
    # Create air alerts
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
    average_12hr['unhealthy_alert'] = average_12hr.apply(unhealthy_air_alert, axis=1)
    # create sensitive HYPOTHTICAL Alert system
        # hypothetical alerts are based on IF everything is reading in PPM
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

    average_12hr['sensitive_alert'] = average_12hr.apply(sensitive_air_alert, axis=1)
    return average_12hr

#-----------------------------------------------------------------------------

# create air df based on 24 hr incriments
def air_24hr_avg(df):
    '''Takes in df df and creates every 8 hour averages'''
    # duplicate datetime column
    df['round_24hr'] = df['datetime']
    # round to every 8 hours
    df['round_24hr'] = df['round_24hr'].dt.round('1440min')
    # create mew df based on the rouned time
    average_24hr = df.groupby('round_24hr', as_index=False).mean()
    # Create AQI for CO
    average_24hr['AQI_CO'] = pd.cut(average_24hr.CO, 
                                bins = [-1,4.5,9.5,12.5,15.5,30.5,4000],
                                labels = ['Good', 'Moderate', 
                                          'Unhealthy for Sensitive Groups', "Unhealthy", 
                                          "Very Unhealthy", 'Hazardous'])
    # Create AQI for Pm2_5
    average_24hr['AQI_pm2_5'] = pd.cut(average_24hr.Pm2_5, 
                                    bins = [-1,12.1,35.5,55.5,150.5,250.5,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # Create AQI for Pm10
    average_24hr['AQI_pm10'] = pd.cut(average_24hr.Pm10, 
                                    bins = [-1,55,154,255,355,425,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for SO2
    average_24hr['AQI_SO2'] = pd.cut(average_24hr.SO2, 
                                    bins = [-1,0.0359,0.0759,0.1859,0.3049,0.6049,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for NO2
    average_24hr['AQI_NO2'] = pd.cut(average_24hr.NO2, 
                                    bins = [-1,0.0539,0.1009,0.3609,0.6499,1.2499,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # create AQI for O3
    average_24hr['AQI_O3'] = pd.cut(average_24hr.O3, 
                                    bins = [-1,0.0549,0.0709,0.0859,0.1059,0.2009,4000],
                                    labels = ['Good', 'Moderate', 
                                              'Unhealthy for Sensitive Groups', "Unhealthy", 
                                              "Very Unhealthy", 'Hazardous'])
    # rename the new date time column
    average_24hr = average_24hr.rename(columns={"round_24hr": "datetime"})
    # Create air alerts
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
    average_24hr['unhealthy_alert'] = average_24hr.apply(unhealthy_air_alert, axis=1)
    # create sensitive HYPOTHTICAL Alert system
        # hypothetical alerts are based on IF everything is reading in PPM
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

    average_24hr['sensitive_alert'] = average_24hr.apply(sensitive_air_alert, axis=1)
    return average_24hr

#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------

# daily COSA
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