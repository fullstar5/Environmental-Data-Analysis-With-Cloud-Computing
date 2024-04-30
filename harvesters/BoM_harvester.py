import logging, json, requests, socket
from collections import defaultdict
from elasticsearch import Elasticsearch

def fetch_weather_data():
    mel_OP_url = "http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json"
    mel_airport_url = "http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94866.json"

    # unusable link, will return 403
    # avalon_url = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94854.json"
    # cerberus_url = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94898.json"
    # coldstream = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94864.json"
    # essendon_airport = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.95866.json"
    # fawkner_beacon = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.95872.json"
    # ferny_creek = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94872.json"
    # frankston_ballamPark = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94876.json"
    # frankston_beach = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94871.json"
    # geelong_racecourse = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94857.json"
    # laverton = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94865.json"
    # moorabbin_airport = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94870.json"
    # point_cook = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.95941.json"
    # point_wilson = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94847.json"
    # rhyll = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94892.json"
    # scoresby = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.95867.json"
    # sheoaks = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94863.json"
    # south_channel_island = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94853.json"
    # st_kilda_harbour_rmys = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.95864.json"
    # viewbank = "http://www.bom.gov.au/fwo/IDV60901/IDV60901.95874.json"

    urls = {"mel_OP_url": mel_OP_url, "mel_airport_url": mel_airport_url}
    ans = defaultdict(dict)
    for key, url in urls.items():
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            ans[key] = data["observations"]["data"][0]
        else:
            ans[key] = None
    return ans


weather_info = fetch_weather_data()
print(json.dumps(weather_info, indent=4))
