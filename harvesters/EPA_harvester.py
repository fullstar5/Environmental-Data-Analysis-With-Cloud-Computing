import requests


def main():
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

    response = requests.get(url, params, headers=headers)

    print(response.status_code)
    print(response.text)


main()
