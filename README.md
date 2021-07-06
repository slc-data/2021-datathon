# 2021-datathon-readme
<a name="top"></a>
![name of photo](url_to_photo)

***
[[Project Description](#project_description)]
[[Project Planning](#planning)]
[[Key Findings](#findings)]
[[Data Dictionaries](#dictionary)]
[[Work Though the Pipeline](#pipeline)]
[[Conclusion](#conclusion)]
[[Recreate This Project](#recreate)]
___


## <a name="project_description"></a> Project Description
![desc](URL to photo)
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
    
    
## <a name="planning"></a> Project Planning
![plan](URl to photo)
[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### Projet Outline:
    
- Acquisiton of data
- Prepare and clean data with python - Jupyter Labs
    - Drop
    - Rename
    - Create
    - Dummies
    - Etc.
- Explore data:
    - What are the features?
    - Null values:
        - Are the fixable or should they just be deleted.
    - Categorical or continuous values.
    - Make graphs that show:
        - At least 2.
- Run statistical analysis:
    - At least 2.
        
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


</details>

    
## <a name="findings"></a> Key Findings
![find](URL to photo)

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
    

### Modeling:
- Baseline:
    - 
- Models Made:
    - 
- Best Model:
    - 
- Model testing:
    - 
- Performance:
    - 

***

    
</details>

## <a name="dictionary"></a> Data Dictionaries
![dict](URL to photo)

[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### SAWS
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| Record | #	Unique Record Number (used to cross reference SAWS internal dataset) | Data Type |
| Prefix | Compass direction associated with street name (N, S, E, W, NE, NW, SE, SW or blank) | Data Type |
| Service Location | Name of street where residential type service account is located | Data Type |
| Suffix | Type associated with street name (ST, RD, DR, CT, LOOP, PKWY, BLVD… etc.) | Data Type |
| ZIP Code | 5-digit zip codes associated with service location | Data Type |
| 17-JAN to 17-DEC | Gallons billed to Customer Account for service location in each month of 2017 | Data Type |
| 18-JAN to 18-DEC | Gallons billed to Customer Account for service location in each month of 2018 | Data Type |
| 19-JAN to 19-DEC | Gallons billed to Customer Account for service location in each month of 2019 | Data Type |
| 20-JAN to 20-DEC | Gallons billed to Customer Account for service location in each month of 2020 | Data Type |

### COSA Air
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| DateTime | Date and Time when the value was read by the sensor in local time | Data Type |
| Pm1_0 | Microgram per meter cube of inhalable particles with diameter smaller than 1 Micron | Data Type |
| Pm2_5 | Microgram per meter cube of inhalable particles with diameter smaller 2.5 Micron | Data Type |
| Pm10 | Microgram per meter cube of inhalable particles with diameter smaller 10 Micron | Data Type |
| SO2 | Sulfuric Dioxide concentration in PPM (parts per million) | Data Type |
| O3 | Ozone concentration in PPM (parts per million) | Data Type |
| CO | Carbone Monoxide concentration in PPM (parts per million) | Data Type |
| NO2 | Nitrogen Dioxide concentration in PPM (parts per million) | Data Type |
| AlertTriggered | A list of measurements that triggered an alert. | Data Type |
| SensorStatus | Indicates the status of the sensor when the reading was taken. | Data Type |


### COSA Flood
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| DateTime | Date and Time when the value was read by the sensor in local time | Data Type |
| Temp(c) | Temperature at sensor in deg C | Data Type |
| Temp(F) | Temperature at sensor in deg F | Data Type |
| DistToWL(ft) | Distance from sensor to water level in ft | Data Type |
| DistToWL(m) | Distance from sensor to water level in m | Data Type |
| DistToDF(ft) | Distance from sensor to dry floor of river, creek etc. (ft) | Data Type |
| DistToDF(m) | Distance from sensor to dry floor of river, creek etc. (m) | Data Type |
| AlertTriggered | Y, N value if sensor supports water level alerts and alert was triggered.   | Data Type |
| SensorStatus | Indicates the status of the sensor when the reading was taken. | Data Type |


### COSA Sound
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| DateTime | Date and Time when the value was read by the sensor in local time | Data Type |
| NoiseLevel(db) | Noise level in decibels (db) | Data Type |
| AlertTriggered | Y, N value if sensor supports alert levels and alert was triggered. | Data Type |
| SensorStatus | Indicates the status of the sensor when the reading was taken. | Data Type |
  

### COSA Weather
    
| Attribute | Definition | Data Type |
| ----- | ----- | ----- | 
| DateTime | Date and Time when the value was read by the sensor in local time | Data Type |
| Temp(c) | Ambient air temperature in deg C | Data Type |
| Temp(F) | Ambient air temperature in deg F | Data Type |
| Humidity(%) | % Relative Humidity (RH) | Data Type |
| DewPoint(c) | Due point in deg C | Data Type |
| DewPoint(F) | Due point in deg F | Data Type |
| Pressure(Pa) | Atmospheric pressure in Pascal (Pa) | Data Type |
| AlertTriggered | A list of measurements that triggered an alert. | Data Type |
| SensorStatus | Indicates the status of the sensor when the reading was taken. | Data Type |
  

***
</details>

## <a name="pipeline"></a> Data Science Pipeline
![pipeline](URL to photo)
[[Back to top](#top)]

<details>
  <summary>Click to expand!</summary>

### Acquire Data:
- 
    
### Prepare Data
- 

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
    
### Stats Test 3:
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


## <a name="conclusion"></a> Conclusion
![conclusion](URL to photo)
[[Back to top](#top)]
<details>
  <summary>Click to expand!</summary>

I found....

With further time...

I recommend...


</details>  


## <a name="Recreate This Project"></a> Recreate the Project
![recreate](URL to Photo)
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

