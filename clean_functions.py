
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
    df = df.drop(columns=['Temp_C', 'DistToDF_m', 'DistToWL_m'])
    # Set to date time format
    df.DateTime = pd.to_datetime(df.DateTime)
    df = df.rename(columns={
        "DateTime": "datetime",
        "Sensor_id": "sensor_id",
        "Vendor": "vendor",
        "SensorModel:" "sensor_model",
        "LAT:" "latitude",
        "LONG:" "longitude",
        "Zone:" "pilot_zone",
        "Temp_F:" "temp_farenheit",
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