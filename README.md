<a name="top"></a>
![name of photo](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/header.png?raw=true)

***
[[Project Description](#project_description)]
[[Meet the Team](#team)]
[[Work Though the Pipeline](#pipeline)]
[[Key Findings](#findings)]
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
- Using the SAWS data set we minimized it to only include the medical center zip code (78229). We will be using this focused SAWS data and using it in conjunction with the COSA Medical Center Air/Weather/Flood/Sound data set to see how the these affects water consumption in the area as well as one another. We will also be doing individual analysis on each data set. For the SAWS data set we aim to find the consumption based on the residential water consumption through the year. For the COSA Air Quality we want to see the quality throughout the days and weeks.

### Goals
- Find out if there is a link between air quality and water consumption in the medical center
- See if the air quality sensor is beneficial to SA.
- See water consumption use time analysis.
- Find peak water consumption times (so in the future what can the city do to combat the peak)
- Find peak poor air quality times/days (so in the future what can the city do to combat the peak)

</details>
    
    
## <a name="Meet the Team"></a>
![team]()
[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### Sam Keeler
![sam](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/team.png?raw=true)
    
### Lori Segovia
    
    
### Caitlyn Carney


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
    
**COSA**
- Drop features
- Create new features through all data sets
- DateTime to date time format
- Drop AlertTriggered for all but air quality
- Replace nulls in AlertTriggered (air quality) with None


### Exploration Findings:
- 

### Stats Test 1:
- What is the test?
    - 
- Why use this test?
    - 
- What is being compared?
    - 
- Reject the null or fail to reject
    - 
- What was learned:
    - 

### Stats Test 2:
- What is the test?
    - 
- Why use this test?
    - 
- What is being compared?
    - 
- Reject the null or fail to reject
    - 
- What was learned:
    - 


***
​
    
</details>    

    
## <a name="findings"></a>
![find](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/key_findings.png?raw=true)

[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### Explore:
- 
    
    
### Stats
- Stat Test 1: 
    - which test:
        - reject of accept null

            
- Stat Test 2: 
    - which test:
        - reject of accept null
    

***

    
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

    
### COSA Air
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| DateTime | Date and Time when the value was read by the sensor in local time | datetime64[ns] |
| Pm1_0 | Microgram per meter cube of inhalable particles with diameter smaller than 1 Micron | int64  |
| Pm2_5 | Microgram per meter cube of inhalable particles with diameter smaller 2.5 Micron | int64  |
| Pm10 | Microgram per meter cube of inhalable particles with diameter smaller 10 Micron | int64 |
| SO2 | Sulfuric Dioxide concentration in PPM (parts per million) | int64  |
| O3 | Ozone concentration in PPM (parts per million) | float64 |
| CO | Carbone Monoxide concentration in PPM (parts per million) | int64  |
| NO2 | Nitrogen Dioxide concentration in PPM (parts per million) | int64  |
| AlertTriggered | A list of measurements that triggered an alert. | object |
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
    
### COSA Flood
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| DateTime | Date and Time when the value was read by the sensor in local time | datetime64[ns] |
| sensor_to_water_feet | Distance from sensor to water level in ft | float64 |
| sensor_to_water_meters | Distance from sensor to water level in m | float64 |
| sensor_to_ground_feet | Distance from sensor to dry floor of river, creek etc. (ft) | float64 |
| sensor_to_ground_meters | Distance from sensor to dry floor of river, creek etc. (m) | float64 |
| flood_depth_feet | Depth of flood waters in feet | float64 |
| flood_depth_meters | Depth of flood waters in meters | float64 |

### COSA Sound
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| DateTime | Date and Time when the value was read by the sensor in local time | datetime64[ns] |
| NoiseLevel_db | Noise level in decibels (db) | int64|
| NoiseLevel_db | Nose levels in severity | category|
  

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

I found....

With further time...

I recommend...


</details>  


## <a name="Recreate This Project"></a>
![recreate](https://github.com/slc-data/2021-datathon/blob/main/photos/readme/recreate.png?raw=true)
[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### 1. Getting started

    
Good luck I hope you enjoy your project!

</details>
    


## 

![Folder Contents](URL to photo)


>>>>>>>>>>>>>>>
.

