<a name="top"></a>
![name of photo](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/new_header.png?raw=true)

***
[[Project Description](#project_description)]
[[Work Though the Pipeline](#pipeline)]
[[Data Dictionaries](#dictionary)]
[[Conclusion](#conclusion)]
[[Recreate This Project](#recreate)]
___


## <a name="project_description"></a> 
![desc](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/project_description.png?raw=true)
[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### Description
- Using the SAWS data set we minimized it to only include the medical center zip code (78229) and the downtown zipcode (78205) as used for the street light sensor pilot. We will be using this focused SAWS data and using it in conjunction with the COSA Medical Center Air/Weather/Flood/Sound data set to see how the these affects water consumption in the area as well as one another. We will also be doing individual analysis on each data set. For the SAWS data set we aim to find the consumption based on the residential water consumption through the year. For the COSA Air Quality we want to see the quality throughout the days and weeks.

### Goals
- Find out if there is a link between air quality and water consumption in the medical center
- See if the air quality sensor is beneficial to SA.
- See water consumption use time analysis.
- Find peak water consumption times (so in the future what can the city do to combat the peak)
- Find peak poor air quality times/days (so in the future what can the city do to combat the peak)

</details>


## <a name="pipeline"></a>
![pipeline](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/ds_pipeline.png?raw=true)
[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>
       
### Hypothesis/Questions
- There is a relationship between sound and air quality (louder sound - construction, traffic, etc)
- The hotter it is the more water consumption there is.
- What is water consumption like during storms vs sunny days?
- Are there spikes in air quality at certain times or days?
- Is air quality and water consumption worse on the weekends?
- How is the air quality after it floods?
- What type of weather has the best air quality?
- As air quality gets worse water consumption goes up.
- Does air quality influence water consumption?
- Can we find indications of "Heat Islands" effects in either medical center or downtown.
    
### Acquire Data:
- Data sets were provided by SAWS and COSA to the 2021 Dataton hosts. All data sets can be found at:
    - https://sites.google.com/geekdom.com/2021-smartsa-datathon-data-cat/home
    
### Prepare Data
**SAWS**
- Limit to only include zipcode 78229
    - This is the zip code covering San Antonio Medical center
- Replace all asterisk's with a 0
- Transpose the data
- Drop columns
- Replace nulls with 0
- Concat Prefix, Suffix, and Service Location into one solid location.
- Forcast 2021 water consumption using tableau
    
**COSA**
- Drop features
- Create new features through all data sets
- DateTime to date time format
- Drop AlertTriggered for all but air quality
- Replace nulls in AlertTriggered (air quality) with None


### Exploration Findings:
- Readings for ozone, SO2, and NO2 are readings really high. I speculate that these are actually reading in ppb rather than ppm as stated in the data dictionary. I theorize this (using ozone as an example) because there are a lot of readings above 1. In ppm 1 put air quality into Hazardous so the 100+ readings at 32 would kill anyone on entering this air. But if it is reading in ppb this would be good air quality.
- None of the COSA datasets line up with any of the other data sets chronologically.
- COSA and SAWS dates do not align with one another.
- COSA and SAWS do not have a common feature.
- PM 10: 
    - concentration readings higher than 40 usually are being picked up earlier in the work week.
        - Mon
        - Tues
- Ozone::
    - Higher readings are not triggering any alerts. Basically anything above 15 is not triggering alerts
        - But there is no way to know the actual AQI for these readings due to the inaccurate measurement of ozone
- Carbon Monoxide:
    - Triggers for readings at 63 and 129. However because there is a jump in readings from 8 to 63 there is no way to see where they actually trigger.
    - Fridays and Sundays have the highest average Carbon Monoxide readings
    - There are significantly more readings in the good range than any other
        - In fact there are only good readings when it comes to daily averages
    - For individual readings 
        - Sunday has the most Hazardous readings
        - Friday has some unhealthy readings and Saturday has some hazardous readings
    - 5 and 6 am have the most hazardous reading throughout the day. But there are still more readings in the good range.
    - There are no daily averages outside of good air quality
- PM 2.5
    - 2 pm has the highest average pm 2.5 reading
    - Peak hours for unhealthy readings is 3 am, 8 am, and 11am
    - There are no reading worse than unhealthy
    - Triggers alerts above 34 but for some reason readings between 69 and 82 are not triggering an alert.
    - It seems like alert triggered is not picking up any of the hazardous readings (Hazardous readings for pm 2.5 is anything above 250.5 there are 3 readings within this range)
- Sound:
    - Sound level is usually Moderate or Loud
    - 4pm-5pm tend to have more recorded time at the ver loud level
    - Hours between 8 and 11 am have a lot of very loud recorded moments.
    - Midnight to 6am is the quietest time in the medical center
    - Tuesdays and Fridays have a lot of recorded moments that were very loud
    - Sundays have the highest number of moderate sound level recorded and the least amount of loud recordings
- SAWS
    - September of 2019 has the most water consumption throughout all months and years.
    - In 2017 the month of August had the highest recorded water consumption.
    - March is the lowest month for water consumption through all 4 years.
    - March, January, and April tend to be on the lower side of water consumption.
    - February was low in 2017 and 2018 but spikes in 2019 and 2020
    - Water consumption was lowest for July in 2019
    - 2019 had the lowest average water consumption.
    - 2020 had the highest average water consumption.
        - this may be due to the pandemic and the higher numbers of people being in the hospital and/or searching for medical help.
    - There does seem to be a steady increase in water consumption when going into summer months such as June, July, August(which has the most gallons consumed over all).
        - Then we start to see a steady decrease going into fall and winter months.
    
***
​
    
</details>    

    
</details>

## <a name="dictionary"></a>
![dict](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/data_dict.png?raw=true)

[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### SAWS
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| Record # | #	Unique Record Number (used to cross reference SAWS internal dataset) | int64 |
| zipcode | zip code of loaction | object |
| location | Compass direction associated with street name (N, S, E, W, NE, NW, SE, SW or blank), name of street where residential type service account is located and type associated with street name (ST, RD, DR, CT, LOOP, PKWY, BLVD… etc.) | object |
| year_month | Month and Year of observation | object |
| gallons_consumed | number of gallons used | object |
| geographical | Location in San Antonio | object |
    
### COSA Air
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| datetime | Date and Time when the value was read by the sensor in local time | datetime64[ns] |
| Pm1_0 | Microgram per meter cube of inhalable particles with diameter smaller than 1 Micron | int64  |
| Pm2_5 | Microgram per meter cube of inhalable particles with diameter smaller 2.5 Micron | int64  |
| Pm10 | Microgram per meter cube of inhalable particles with diameter smaller 10 Micron | int64 |
| SO2 | Sulfuric Dioxide concentration in PPM (parts per million) | int64  |
| O3 | Ozone concentration in PPM (parts per million) | float64 |
| CO | Carbone Monoxide concentration in PPM (parts per million) | int64  |
| NO2 | Nitrogen Dioxide concentration in PPM (parts per million) | int64  |
| alert_triggered | A list of measurements that triggered an alert. | object |
| dates | Date of recording | object |
| time | Time of recording | object |
| hour | Hour of the day observation was made | int64 |
| weekday | Whcih day of the week recoding took place | int64 |
| AQI_CO | Air Quality Index of individual recording for carbon monoxide| category |
| CO_24hr | Average carbon Monoxide levels for the day | float64 |
| AQI_CO_24hr | Air Quality Index of daily average carbon monoxide levels | category |
| AQI_pm2_5 | Air Quality Index of individual recording for particles at 2.5 micron | category |
| Pm_25_24hr | Average levels of particles at 2.5 micron for the day| float64 |
| AQI_pm_25_24hr | Air Quality Index of daily average partices at 2.5 micron | category |
| AQI_pm10 | Air Quality Index of individual recording for particles at 10 micron | category |
| Pm_10_24hr | Average levels of particles at 10 micron for the day | float64 |
| AQI_pm10_24hr | Air Quality Index of daily average partices at 10 micron | category | 
| unhealthy_alert | Reconfigured alerts to alert to air quality measure at an unhealthy level or higher (reading CO, Pm 2.5 and 10) | onject |
| sensitive_alert | Reconfigured alerts to alert to air quality measure at an unhealthy level for sensitve groups or higher (reading CO, Pm 2.5 and 10) | onject |
    
** We also created 2 features for both new alerts for how the data dictionary says eveything is read (reading SO2, NO2, O3, CO, Pm 2.5 and 10)
    
### COSA Flood
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| datetime | Date and Time when the value was read by the sensor in local time | datetime64[ns] |
| sensor_to_water_feet | Distance from sensor to water level in ft | float64 |
| sensor_to_water_meters | Distance from sensor to water level in m | float64 |
| sensor_to_ground_feet | Distance from sensor to dry floor of river, creek etc. (ft) | float64 |
| sensor_to_ground_meters | Distance from sensor to dry floor of river, creek etc. (m) | float64 |
| flood_depth_feet | Depth of flood waters in feet | float64 |
| flood_depth_meters | Depth of flood waters in meters | float64 |
| flood_alert | Fixed alert to flooding (reading in meters) | float64 |
    

### COSA Sound
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| DateTime | Date and Time when the value was read by the sensor in local time | datetime64[ns] |
| NoiseLevel_db | Noise level in decibels (db) | int64|
| how_loud | Nose levels in laymen's terms | category|
| sound_alert | Nose levels in severity | category|
  

### COSA Weather
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| datetime | Date and Time when the value was read by the sensor in local time | datetime64[ns] |
| celsius | Ambient air temperature in deg C | float64 |
| farenheit | Ambient air temperature in deg F | float64 |
| humidity | % Relative Humidity (RH) | float64 |
| dewpoint_celsius | Due point in deg C | float64 |
| dewpoint_farenheit | Due point in deg F |float64 |
| pressure | Atmospheric pressure in Pascal (Pa) | float64 |
| time | Time of reading | object |
| date | Date of reading | object |
| weather | What the weather was like outside | object |
| wind | Wind speed in miles per hour | object |
| visibility | visibility in miles| object |
  

***
</details>


## <a name="conclusion"></a>
![conclusion](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/conclusion.png?raw=true)
[[Back to top](#top)]
<details>
  <summary>Click to expand!</summary>

We found....
- None of the 4 data sets from COSA line up together chronologically.
- SAWS data and COSA had no commonality between them.
- Dates dont work between the industries.
    - SAWS data set time frame runs in year-month incriments from January 2017 to December 2020
    - COSA data fruns from April 20th, 2021 to July 8th,2021
- Readings for O3 SO2 and NO2 were readind EXTREMEMLY high (high enough to where you would die upon breathing the air)
    - We theorized:
        - That the sesors are reading these in PPB rather than in PPM
            - This is important because a reading in PPM for Ozone at 32 (will kill you pretty much instantly.
                - Note that there are over 100 readings for ozeone at 32 in PPM.
            - But a reading for PPD for Ozone at 32 is a moderate air quality
- COSA weather data does not actually provide what weather was being experienced that day.
- Alerts for COSA's flood, sound, and weather were all reading as none.
- Alerts for COSA's air quality were very spartic and not picking up all redings above the point alerts started.
    
We believe...
- That by incorperating the changes we made to both the COSA data as well as the SAWS data set: 
    - We will be able to find how sound, weather, flooding, and air quality affect water consumption.
    - Forsee future issues to help create mitigaton tactics to lessen affects on health, costs, and damages. 
    - Create a way to easily see how each industry affects others and how they can help one another.
    - We could create an open source for citizens to gain access to when there are health and saftey issues in the area.

We recommend for COSA...
- Looking into and Reconfiguring O3, NO2, and SO2 measurmet readings to.
    - If they are not reading in ppm converting them to ppm
    - If they are reading in ppm look into the sensors and why it is reading at such a deadly rate.
- Reconfiguring the aler systems for air quality, flooding, and noise level.
    - Code for this can be found in cosa_recommended.py
- Adding features such as
    - Air quality index for each particles individual reading as well as average daily readings.
        - Code for this can be found in cosa_recommended.py (minus so2, no2, and o3)
    - Sound level in layman's terms
        - Code for this can be found in cosa_recommended.py
    - Flood depth
        - Code for this can be found in cosa_recommended.py
    
We recommend for SAWS...
- Reformat your data set layout.
    - Code for all of the following can be found in saws_recommended.py
        - Put year-month in one column instead of the 48 you currently have
        - add a datetime format rather than just 17-JAN


</details>  


## <a name="Recreate This Project"></a>
![recreate](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/recreate.png?raw=true)
[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### 1. Getting started
- Download:
    - SAWS Residential Consumption Data 2 of 3
    - COSA Medical Center Air Quality
    - COSA Medical Center Flood
    - COSA Medical Center Sound Level
    - COSA Medical Center Weather
- Limit the SAWS data to only include zipcode 78229 (the medical center)
- Forcast 2021 data using 2017, 2018, 2019, and 2020 water consumption.
    
Good luck I hope you enjoy your project!

</details>
    


>>>>>>>>>>>>>>>
.

