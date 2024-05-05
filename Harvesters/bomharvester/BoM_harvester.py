import urllib3.exceptions
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests
from elasticsearch import Elasticsearch


def main():
    mel_OP_url = "http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json"
    mel_airport_url = "http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94866.json"

    # connect and login into elasticsearch
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

    urls = {"mel_OP_url": mel_OP_url, "mel_airport_url": mel_airport_url}

    for key, url in urls.items():
        try:
            response = requests.get(url)
            data = response.json()
            # print(json.dumps(data, indent=4))
        except Exception as e:
            print("error when request BoM data: ",  e)
            return 500

        # extracting data
        site_name = data["observations"]["data"][0]["name"]
        local_date_time = data["observations"]["data"][0]["local_date_time_full"]
        coordinates = [data["observations"]["data"][0]["lat"], data["observations"]["data"][0]["lon"]]
        apparent_temperature = data["observations"]["data"][0]["apparent_t"]
        cloud = data["observations"]["data"][0]["cloud"]
        cloud_type = data["observations"]["data"][0]["cloud_type"]
        delta_temperature = data["observations"]["data"][0]["delta_t"]  # Air temperature minus wet bulb temperature
        air_temperature = data["observations"]["data"][0]["air_temp"]
        dew_point = data["observations"]["data"][0]["dewpt"]  # either wet and dry bulb temperature (preferred)
        press = data["observations"]["data"][0]["press"]
        press_tend = data["observations"]["data"][0]["press_tend"]
        rain_trace = data["observations"]["data"][0]["rain_trace"]
        swell_period = data["observations"]["data"][0]["swell_period"]
        vis_km = data["observations"]["data"][0]["vis_km"]  # Visibility
        weather = data["observations"]["data"][0]["weather"]
        if weather == "-":
            weather = "Fine"
        wind_spd_kmh = data["observations"]["data"][0]["wind_spd_kmh"]

        # build document
        doc = {
            "site_name": site_name,
            "local_date_time": local_date_time,
            "coordinates": coordinates,
            "apparent_temperature": apparent_temperature,
            "cloud": cloud,
            "cloud_type": cloud_type,
            "delta_temperature": delta_temperature,
            "air_temperature": air_temperature,
            "dew_point": dew_point,
            "press": press,
            "press_tend": press_tend,
            "rain_trace": rain_trace,
            "swell_period": swell_period,
            "vis_km": vis_km,
            "weather": weather,
            "wind_spd_kmh": wind_spd_kmh,
        }
        local_date = data["observations"]["data"][0]["local_date_time_full"][:8]
        index_name = f"bom-weather-{local_date}"
        unique_id = f"{site_name}-{local_date_time}"
        # try:
        #     client.index(index=index_name, id=unique_id, body=doc)
        # except Exception as e:
        #     print("Error inserting into Elasticsearch: ", e)
        #     return 500

        print(unique_id, index_name)
    print("insert complete")
    return 200


main()