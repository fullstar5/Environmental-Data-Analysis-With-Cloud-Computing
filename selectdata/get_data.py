
def twitter(es, city=None, size=1000, language=None):

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
        # "_source": ['language'],
        "query": query_part
    }
    
    response = es.search(index="twitter_vic", body=query)

    hits = response['hits']['hits']
    
    return hits

