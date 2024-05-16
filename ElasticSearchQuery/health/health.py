from flask import request, jsonify, current_app
from elasticsearch import Elasticsearch

def main():
    """
    Search health-related data from a specific index.
    
    Parameters:
        asr (str, optional): Filter by Age-Standardised Rate (ASR). Defaults to None.
        disease (str, optional): Filter by disease name. Defaults to None.
        lga (str, optional): Filter by Local Government Area (LGA). Defaults to None.
        num (int, optional): Filter by numerical value related to health data. Defaults to None.
        period (str, optional): Filter by time period of the data. Defaults to None.
        phn (str, optional): Filter by Primary Health Network (PHN). Defaults to None.
        sr (str, optional): Filter by specific rate. Defaults to None.
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
    
    asr = request.args.get('asr',None)
    disease = request.args.get('disease',None)
    lga = request.args.get('lga',None)
    num = request.args.get('num',None)
    period = request.args.get('period',None)
    phn = request.args.get('phn',None)
    sr = request.args.get('sr',None)
    size = request.args.get('size', 1000)

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
    
    return jsonify(response['hits']['hits'])
