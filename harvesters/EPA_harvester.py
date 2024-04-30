import requests, json
from flask import current_app
from elasticsearch import Elasticsearch


def main():
    # connect and login into elasticsearch
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        basic_auth=('elastic', 'elastic')
    )
    # current_app.logger.info(f'begin harvesting to add')

    # retrieve EPA air quality from website
    environmentalSegment_air = "air"
    environmentalSegment_water = "water"
    siteID = "e47fa291-45de-4b06-b6ac-6bb8bf6421f8"
    url = "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites"
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
        return

    # extracting data
    data_time = data["records"][0]["siteHealthAdvices"][0]["since"]
    data_day = data_time.split("T")[0]
    data_hour = data_time.split("T")[1].split("Z")[0]
    print(data_time)
    print(data_day)
    print(data_hour)

    index_name = f"EPA-air-quality-{data_day}"

    total_avgValue = 0
    total_cityCount = 0
    for record in data["records"]:
        # ignore camera type
        if record["siteType"] == "Camera":
            continue

        total_cityCount += 1
        site_name = record["siteName"]
        coordinates = record["geometry"]["coordinates"]

        site_health_advices = record["siteHealthAdvices"][0]
        if site_health_advices:
            healthParameter = site_health_advices.get("healthParameter", "PM2.5")
            averageValue = site_health_advices.get("averageValue", total_avgValue/total_cityCount)
            total_avgValue += averageValue
            healthAdvice = site_health_advices.get("healthAdvice", "Good")
        else:
            healthParameter = "PM2.5"
            averageValue = total_avgValue/total_cityCount
            total_avgValue += averageValue
            healthAdvice = "Good"

        # build elastic search doc and insert into right index (distinct by day)
        doc = {
            "hour": data_hour,
            "siteName": site_name,
            "coordinates": coordinates,
            "averageValue": averageValue,
            "healthParameter": healthParameter,
            "healthAdvice": healthAdvice,
        }
        client.index(index=index_name, body=doc)
    # print(response.text)


main()
