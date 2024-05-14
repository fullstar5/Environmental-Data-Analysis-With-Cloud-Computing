import json
from elasticsearch import Elasticsearch

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def upload_data(es, data):
    for region, areas in data.items():
        for area, periods in areas.items():
            for period, diseases in periods.items():
                bbox = diseases.pop("bbox", None)
                for disease, stats in diseases.items():
                    doc_id = f"{region}-{area}-{period}-{disease}"
                    document = {
                        "region": region,
                        "area": area,
                        "period": period,
                        "disease": disease,
                        "stats": stats,
                        "bbox": bbox
                    }
                    es.index(index="health_data", id=doc_id, body=document)
                    print(f"Document {doc_id} uploaded successfully!")

def main():
    es = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic'),
        request_timeout=100,
        ssl_show_warn=False
    )

    if not es.indices.exists(index="health_data"):
        es.indices.create(index="health_data", ignore=400)

    data = load_data('Users/yueyangwu/Desktop/CCC2/sorted_newData/add_PHN/PM.json')
    upload_data(es, data)

if __name__ == "__main__":
    main()


