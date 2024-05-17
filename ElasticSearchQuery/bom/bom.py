from flask import request, jsonify, current_app
from elasticsearch import Elasticsearch

def main():
    """
    Must have start and end date. (from 3)

    Search for Bureau of Meteorology (BOM) weather data over a specified date range.
    
    Parameters:
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
        JSON of hits from the query.
    """
    current_app.logger.info(f'Received request: ${request.headers}')

    try:
        es = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            basic_auth=('elastic', 'elastic'),
            request_timeout=60,
            ssl_show_warn=False
        )
    except Exception as e:
        print("Error when connect with ES: ", e)
        return 500
    
    start = request.args.get('start',3,type=int)
    end = request.args.get('end',start,type=int)
    air_temp = request.args.get('air_temp',None)
    apparent_temp = request.args.get('appartent_temp',None)
    cloud = request.args.get('cloud',None)
    cloud_type = request.args.get('cloud_type',None)
    delta_temp = request.args.get('delta_temp',None)
    dew_point = request.args.get('dew_point',None)
    time = request.args.get('time',None)
    press = request.args.get('press',None)
    press_tend = request.args.get('press_tend',None)
    rain_trace = request.args.get('rain_trace',None)
    vis_km = request.args.get('vis_km',None)
    weather = request.args.get('weather',None)
    wind_spd_kmh = request.args.get('wind_spd_kmh',None)
    size = request.args.get('size', 1000)

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
    
    return jsonify(response['hits']['hits'])
