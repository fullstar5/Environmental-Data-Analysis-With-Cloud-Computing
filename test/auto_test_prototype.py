import urllib3.exceptions
import requests
from elasticsearch import Elasticsearch

def test_ES_connection():
    try:
        client = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            basic_auth=('elastic', 'elastic'),
            timeout=60,
            ssl_show_warn=False
        )
    except Exception as e:
        print("error when connect with ES: ", e)
        return 500
    return 200

def test_url_connection(url):
    params = {
        "environmentalSegment": environmentalSegment_air
    }
    headers = {
        "User-Agent": 'curl/8.4.0',
        "Cache-Control": 'no-cache',
        "X-API-Key": "62eb03b279a54273ace3f893e994f90d"
    }
    try:
        response = requests.get(url, params, headers=headers)
        data = response.json()
    except Exception as e:
        print("error when request EPA data: ", e)
        return 500
    return 200

def test_bom_url(url):
    try:
        response = requests.get(url)
        # print(json.dumps(data, indent=4))
    except Exception as e:
        print("error when request BoM data: ",  e)
        return 500
    return 200