#get_data.py: Fuctions of searching for data via ES
"""
All functions must have 'es' when used, all results will be stored in a list.
                         ↓↓
es = Elasticsearch(
    'https://127.0.0.1:9200',
    verify_certs=False,
    basic_auth=('elastic', 'elastic'),
    request_timeout=60,
    ssl_show_warn=False
    )
"""


def twitter(es, city=None, size=1000, language=None):
    # from get_data import twitter
    """
    Search for Twitter-like data within specified indices.
    
    Parameters:
        es (Elasticsearch): Elasticsearch connection object.
        city (str, optional): Filter results by city. Defaults to None.
        size (int, optional): Number of results to return. Defaults to 1000.
        language (str, optional): Filter results by language. Defaults to None.
        
    Returns:
        list: List of hits from the query.
    """

    index_names = "twitter_vic,twitter_vic_529176" 

    must_conditions = []

    if city:
        must_conditions.append({"match": {"full_name": city}})
    if language:
        must_conditions.append({"match": {"language": language}})


    if must_conditions:
        query_part = {"bool": {"must": must_conditions}}
    else:
        query_part = {"match_all": {}}
    

    query = {
        "size": size,
        "query": query_part
    }
    
    response = es.search(index=index_names, body=query)

    hits = response['hits']['hits']
    
    return hits


def epa(es, start, end, avg=None, time=None, health_advice=None, city=None, health_parameter=None, size=1000):
    # from get_data import epa
    """
    e.g.: results = epa(es, 1, 5)
    must have start and end date.
    start: start date, end: end date. (from 1)

    Search EPA air quality data within a date range in specified indices.
    
    Parameters:
        es (Elasticsearch): Elasticsearch connection object.
        start (int): Start day of the month for the query.
        end (int): End day of the month for the query.
        avg (float, optional): Filter by average value. Defaults to None.
        time (str, optional): Filter by time of day. Defaults to None.
        health_advice (str, optional): Filter by health advice. Defaults to None.
        city (str, optional): Filter by city. Defaults to None.
        health_parameter (str, optional): Filter by specific health parameter. Defaults to None.
        size (int, optional): Number of results to return. Defaults to 1000.
        
    Returns:
        list: List of hits from the query.
    """

    must_conditions = []

    index_names = ",".join([f"epa-air-quality-2024-05-{str(i).zfill(2)}" for i in range(start, end+1)])

    if avg:
        must_conditions.append({"match": {"averageValue": avg}})
    if time:
        must_conditions.append({"match": {"hour": time}})
    if health_advice:
        must_conditions.append({"match": {"healthAdvice": health_advice}})
    if city:
        must_conditions.append({"match": {"siteName": city}})
    if health_parameter:
        must_conditions.append({"match": {"healthParameter": health_parameter}})


    if must_conditions:
        query_part = {"bool": {"must": must_conditions}}
    else:
        query_part = {"match_all": {}}


    query = {
        "size": size,
        "query": query_part
    }
    
    response = es.search(index=index_names, body=query)

    hits = response['hits']['hits']
    
    return hits


def bom(es, start, end, air_temp=None, apparent_temp=None, cloud=None, cloud_type=None, delta_temp=None, dew_point=None, time=None, press=None, press_tend=None, rain_trace=None, vis_km=None, weather=None, wind_spd_kmh=None, size=1000):
    # from get_data import bom
    """
    e.g.: results = bom(es, 3, 10)
    Must have start and end date. (from 3)

    Search for Bureau of Meteorology (BOM) weather data over a specified date range.
    
    Parameters:
        es (Elasticsearch): Elasticsearch connection object.
        start (int): Start day of the query period.
        end (int): End day of the query period.
        air_temp (float, optional): Filter by air temperature. Defaults to None.
        apparent_temp (float, optional): Filter by apparent temperature. Defaults to None.
        cloud (str, optional): Filter by cloud coverage description. Defaults to None.
        cloud_type (str, optional): Filter by type of clouds. Defaults to None.
        delta_temp (float, optional): Filter by temperature change. Defaults to None.
        dew_point (float, optional): Filter by dew point. Defaults to None.
        time (str, optional): Filter by specific time. Defaults to None.
        press (float, optional): Filter by pressure. Defaults to None.
        press_tend (str, optional): Filter by pressure tendency. Defaults to None.
        rain_trace (str, optional): Filter by rain trace amounts. Defaults to None.
        vis_km (str, optional): Filter by visibility in kilometers. Defaults to None.
        weather (str, optional): Filter by general weather conditions. Defaults to None.
        wind_spd_kmh (float, optional): Filter by wind speed in km/h. Defaults to None.
        size (int, optional): Number of results to return. Defaults to 1000.
        
    Returns:
        list: List of hits from the query.
    """

    must_conditions = []

    index_names = ",".join([f"bom-weather-202405{str(i).zfill(2)}" for i in range(start, end+1)])

    if air_temp:
        must_conditions.append({"match": {"air_temperature": air_temp}})
    if apparent_temp:
        must_conditions.append({"match": {"apparent_temperature": apparent_temp}})
    if cloud:
        must_conditions.append({"match": {"cloud": cloud}})
    if cloud_type:
        must_conditions.append({"match": {"cloud_type": cloud_type}})
    if delta_temp:
        must_conditions.append({"match": {"delta_temperature": delta_temp}})
    if dew_point:
        must_conditions.append({"match": {"dew_point": dew_point}})
    if time:
        must_conditions.append({"match": {"time": time}})
    if press:
        must_conditions.append({"match": {"press": press}})
    if press_tend:
        must_conditions.append({"match": {"press_tend": press_tend}})
    if rain_trace:
        must_conditions.append({"match": {"rain_trace": rain_trace}})
    if vis_km:
        must_conditions.append({"match": {"vis_km": vis_km}})
    if weather:
        must_conditions.append({"match": {"weather": weather}})
    if wind_spd_kmh:
        must_conditions.append({"match": {"wind_spd_kmh": wind_spd_kmh}})

    if must_conditions:
        query_part = {"bool": {"must": must_conditions}}
    else:
        query_part = {"match_all": {}}


    query = {
        "size": size,
        "query": query_part
    }
    
    response = es.search(index=index_names, body=query)

    hits = response['hits']['hits']
    
    return hits


def health(es, asr=None, disease=None, lga=None, num=None, period=None, phn=None, sr=None, size=1000):
    # from get_data import health
    """
    e.g.results = health(es, phn="North Western Melbourne", size=5)
    default size is 1000
    
    Search health-related data from a specific index.
    
    Parameters:
        es (Elasticsearch): Elasticsearch connection object.
        asr (str, optional): Filter by Age-Standardised Rate (ASR). Defaults to None.
        disease (str, optional): Filter by disease name. Defaults to None.
        lga (str, optional): Filter by Local Government Area (LGA). Defaults to None.
        num (int, optional): Filter by numerical value related to health data. Defaults to None.
        period (str, optional): Filter by time period of the data. Defaults to None.
        phn (str, optional): Filter by Primary Health Network (PHN). Defaults to None.
        sr (str, optional): Filter by specific rate. Defaults to None.
        size (int, optional): Number of results to return. Defaults to 1000.
        
    Returns:
        list: List of hits from the query.
    """

    must_conditions = []

    if asr:
        must_conditions.append({"match": {"ASR": asr}})
    if disease:
        must_conditions.append({"match": {"Disease": disease}})
    if lga:
        must_conditions.append({"match": {"LGA": lga}})
    if num:
        must_conditions.append({"match": {"NUM": num}})
    if period:
        must_conditions.append({"match": {"Period": period}})
    if phn:
        must_conditions.append({"wildcard": {"PHN": "*"+ phn + "*"}})
    if sr:
        must_conditions.append({"match": {"SR": sr}})


    if must_conditions:
        query_part = {"bool": {"must": must_conditions}}
    else:
        query_part = {"match_all": {}}


    query = {
        "size": size,
        "query": query_part
    }
    
    response = es.search(index="health_data", body=query)

    hits = response['hits']['hits']
    
    return hits
