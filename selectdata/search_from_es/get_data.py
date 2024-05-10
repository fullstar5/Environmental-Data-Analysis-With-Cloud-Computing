#get_data.py: fuctions of searching for data via ES
"""
All functions must have 'es' when used, all results will be stored in a dict.
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
    e.g.: results = twitter(es, city="Ballarat", size=5, language="de")
    default size is 1000
    Add whatever u want to search for (city or language or both).
    """
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
    
    response = es.search(index="twitter_vic", body=query)

    hits = response['hits']['hits']
    
    return hits


def epa(es, start, end, avg=None, time=None, health_advice=None, city=None, health_parameter=None, size=1000):
    # from get_data import epa
    """
    e.g.: results = epa(es, 1, 5)
    must have start and end date.
    start: start date, end: end date.
                ↓
                1
    default size is 1000
    Add whatever u want to search for.
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
    must have start and end date.
    start: start date, end: end date.
                ↓
                3
    default size is 1000
    Add whatever u want to search for.
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
    Add whatever u want to search for.
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
        must_conditions.append({"match": {"PHN": phn}})
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
