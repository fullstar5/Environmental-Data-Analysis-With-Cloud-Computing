# API

## BOM

### Request
`GET /bom[?start][&end][&air_temp][&apparent_temp][&cloud][&cloud_type][&delta_temp][&dew_point][&time][&press][&press_tend][&rain_trace][&vis_km][&weather][&wind_spd_kmh][&size]`

### Description
This endpoint retrieves Bureau of Meteorology (BOM) weather data over a specified date range. It allows users to filter the search results based on air temperature, apparent temperature, cloud coverage, cloud type, temperature change, dew point, time, pressure, pressure tendency, rain trace amounts, visibility in kilometers, general weather conditions, and wind speed.

### Request Parameters
- **start**: Required. The start day of the query period (integer).
- **end**: Optional. The end day of the query period (integer). Defaults to the same as start.
- **air_temp**: Optional. Filter by air temperature (float).
- **apparent_temp**: Optional. Filter by apparent temperature (float).
- **cloud**: Optional. Filter by cloud coverage description (string).
- **cloud_type**: Optional. Filter by type of clouds (string).
- **delta_temp**: Optional. Filter by temperature change (float).
- **dew_point**: Optional. Filter by dew point (float).
- **time**: Optional. Filter by specific time (string).
- **press**: Optional. Filter by pressure (float).
- **press_tend**: Optional. Filter by pressure tendency (string).
- **rain_trace**: Optional. Filter by rain trace amounts (string).
- **vis_km**: Optional. Filter by visibility in kilometers (string).
- **weather**: Optional. Filter by general weather conditions (string).
- **wind_spd_kmh**: Optional. Filter by wind speed in km/h (float).
- **size**: Optional. The number of results to return (integer). Defaults to 1000.

### Response
A JSON object of hits, each representing a weather data entry that matches the search criteria.

### Error Codes
- **500 Internal Server Error**: Could not connect to the Elasticsearch cluster.

## EPA

### Request
`GET /epa[?start][&end][&avg][&time][&health_advice][&city][&health_parameter][&size]`

### Description
This endpoint retrieves air quality data saved in Elasticsearch for a specified date range. It allows users to filter the search results based on average value, time of day, health advice, city, and specific health parameters.

### Request Parameters
- **start**: Required. The start day for the query (integer).
- **end**: Optional. The end day for the query (integer). Defaults to the same as start.
- **avg**: Optional. The average value to filter results (float).
- **time**: Optional. The hour to filter results (string).
- **health_advice**: Optional. The health advice to filter results (string).
- **city**: Optional. The siteName to filter results (string).
- **health_parameter**: Optional. The specific health parameter to filter results (string).
- **size**: Optional. The number of results to return (integer). Defaults to 1000.

### Response
A JSON object of hits, each representing an air quality data entry that matches the search criteria.

### Error Codes
- **500 Internal Server Error**: Could not connect to the Elasticsearch cluster.

## Health

### Request
`GET /health[?asr][&disease][&lga][&num][&period][&phn][&sr][&size]`

### Description
This endpoint searches health-related data. It allows users to filter the search results by Age-Standardised Rate (ASR), disease name, Local Government Area (LGA), number of deaths, time period, Primary Health Network (PHN), and Standardized Rate (SR).

### Request Parameters
- **asr**: Optional. The Age-Standardised Rate (ASR) to filter the search results (string). Defaults to None.
- **disease**: Optional. The disease name to filter the search results (string). Defaults to None.
- **lga**: Optional. The Local Government Area (LGA) to filter the search results (string). Defaults to None.
- **num**: Optional. The number of deaths to filter the search results (integer). Defaults to None.
- **period**: Optional. The time period to filter the search results (string). Defaults to None.
- **phn**: Optional. The Primary Health Network (PHN) to filter the search results (string). Defaults to None.
- **sr**: Optional. The Standardized Rate (SR) to filter the search results (string). Defaults to None.
- **size**: Optional. The number of results to return (integer). Defaults to 1000.

### Response
A JSON object of hits, each representing a health-related data entry that matches the search criteria.

### Error Codes
- **500 Internal Server Error**: Could not connect to the Elasticsearch cluster.


## Twitter

### Request
`GET /twitter[?city][&size][&language]`

### Description
This endpoint searches for Twitter data within specified indices. It allows users to filter the search results by city and language.

### Request Parameters
- **city**: Optional. The city to filter the search results (string). Defaults to None.
- **size**: Optional. The number of results to return (integer). Defaults to 1000.
- **language**: Optional. The language to filter the search results (string). Defaults to None.

### Response
A JSON object of hits, each representing a Twitter  data entry that matches the search criteria.

### Error Codes
- **500 Internal Server Error**: Could not connect to the Elasticsearch cluster.
