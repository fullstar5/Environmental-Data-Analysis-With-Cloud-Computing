import json
from elasticsearch import Elasticsearch, helpers

def load_data(file_path):

    with open(file_path, 'r') as file:
        return json.load(file)

def transform_data(data):

    actions = []
    for region, areas in data.items():
        for area, periods in areas.items():
            for period, diseases in periods.items():
                bbox = diseases.pop("bbox", None) 
                for disease, stats in diseases.items():
                    action = {
                        "_index": "health_data",
                        "_type": "_doc",
                        "_source": {
                            "region": region,
                            "area": area,
                            "period": period,
                            "disease": disease,
                            "stats": stats,
                            "bbox": bbox
                        }
                    }
                    actions.append(action)
    return actions

def main():
    # connect and login into elasticsearch
    try:
        es = Elasticsearch(
            'https://elasticsearch-master.elastic.svc.cluster.local:9200',
            verify_certs=False,
            basic_auth=('elastic', 'elastic'),
            timeout=100,
            ssl_show_warn=False
        )
    except Exception as e:
        print("error when connect with ES: ", e)
        return 500

    if not es.indices.exists(index="health_data"):
        es.indices.create(index="health_data")

    data = load_data('/Users/yueyangwu/Desktop/CCC2/sorted_newData/add_PHN/PM.json')  

    actions = transform_data(data)

    helpers.bulk(es, actions)
    print("Data uploaded successfully!")

if __name__ == "__main__":
    main()
