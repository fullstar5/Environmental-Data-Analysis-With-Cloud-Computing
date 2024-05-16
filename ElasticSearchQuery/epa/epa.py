from flask import request, jsonify, current_app
from elasticsearch import Elasticsearch

def main():
    """
    must have start and end date.
    start: start date, end: end date. (from 1)

    Search EPA air quality data within a date range in specified indices.
    
    Parameters:
        start (int): Start day of the month for the query.
        end (int): End day of the month for the query.
        avg (float, optional): Filter by average value. Defaults to None.
        time (str, optional): Filter by time of day. Defaults to None.
        health_advice (str, optional): Filter by health advice. Defaults to None.
        city (str, optional): Filter by city. Defaults to None.
        health_parameter (str, optional): Filter by specific health parameter. Defaults to None.
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
    
    start = request.args.get('start',1)
    end = request.args.get('end',start)
    avg = request.args.get('avg',None)
    time = request.args.get('time',None)
    health_advice = request.args.get('health_advice',None)
    city = request.args.get('city',None)
    health_parameter = request.args.get('health_parameter',None)
    size = request.args.get('size', 1000)

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
    
    return jsonify(response['hits']['hits'])
