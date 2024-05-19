from flask import request, jsonify, current_app
from elasticsearch import Elasticsearch

def main():
    """
    Search for Twitter-like data within specified indices.
    
    Parameters:
        city (str, optional): Filter results by city. Defaults to None.
        size (int, optional): Number of results to return. Defaults to 1000.
        language (str, optional): Filter results by language. Defaults to None.
        
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
    
    city = request.args.get('city',None)
    size = request.args.get('size', 1000)
    language = request.args.get('language',None)

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
    
    return jsonify(response['hits']['hits'])
