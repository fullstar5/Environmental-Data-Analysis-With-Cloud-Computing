from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__) 
      
try:
    client = Elasticsearch(
        'https://127.0.0.1:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic'),
        request_timeout=60,
        ssl_show_warn=False
    )
except Exception as e:
    print("error when connect with ES: ", e)


def construct_query(params):
    query = {"bool": {"must": []}}
    p = 0

    if params["healthAdvice"]:
        query["bool"]["must"].append({"match": {"healthAdvice": params["healthAdvice"]}})
        p += 1

    if params["averageValue"]:
        query["bool"]["must"].append({"match": {"averageValue": params["averageValue"]}})
        p += 1

    if params["healthParameter"]:
        query["bool"]["must"].append({"match": {"healthParameter": params["healthParameter"]}})
        p += 1

    if params["siteName"]:
        query["bool"]["must"].append({"match": {"siteName": params["siteName"]}})
        p += 1

    if p == 0:
        return None
    return query

@app.route('/air/dates/')
def getDates():
    indices = client.cat.indices(format='json')
    dates = []
    for index in indices:
        name = index['index']
        if 'epa-air-quality' in name:
            dates.append(name[16:])
    return jsonify(dates)
    
@app.route('/air')
def getData():
    start = request.args.get("startDate",'01')
    end = request.args.get("endDate", start)
    indices = []
    for i in range(int(start),int(end)+1):
        indices.append('epa-air-quality-2024-05-'+'{:02d}'.format(i))

    # construct params
    params = {
        "healthAdvice": request.args.get("healthAdvice", None),
        "averageValue": request.args.get("averageValue", None),
        "healthParameter": request.args.get("healthParameter", None),
        "siteName": request.args.get("siteName", None),
    }
    
    res = client.search(index=indices, query=construct_query(params))
    data = res['hits']
    return jsonify(data)
    
if __name__ == "__main__":
    app.run(debug=True)
