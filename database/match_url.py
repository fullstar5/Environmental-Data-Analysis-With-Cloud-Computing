'''
-----------Team 48------------
| Name          | Student ID |
|---------------|------------|
| Yifei ZHANG   | 1174267    |
| Yibo HUANG    | 1380231    |
| Hanzhang SUN  | 1379790    |
| Liyang CHEN   | 1135879    |
| Yueyang WU    | 1345511    |
'''
#match_url.py: get data from es via ReSTful API
import requests

def twitter(city=None, size=2000, language=None):

    twitter_url = 'http://127.0.0.1:9090/twitter'

    params = {
        'city': city,
        'language': language,
        'size': size,
    }

    twitter = requests.get(twitter_url, params=params)
    twitter_data = twitter.json()
    data_twitter = [item['_source'] for item in twitter_data]
    
    return data_twitter

def epa(start=3, end=10, avg=None, time=None, health_advice=None, city=None, health_parameter=None, size=2000):

    epa_url = 'http://127.0.0.1:9090/epa'

    params = {
        'start': start,
        'end': end,
        'avg': avg,
        'time': time,
        'health_advice': health_advice,
        'city': city,
        'health_parameter': health_parameter,
        'size': size,
    }

    epa = requests.get(epa_url, params=params)
    epa_data = epa.json()
    data_epa = [{**item['_source'], 'date': item['_index']} for item in epa_data]
    
    return data_epa


def bom(start=3, end=10, air_temp=None, apparent_temp=None, cloud=None, cloud_type=None, delta_temp=None, dew_point=None, time=None, press=None, press_tend=None, rain_trace=None, vis_km=None, weather=None, wind_spd_kmh=None, size=2000):

    bom_url = 'http://127.0.0.1:9090/bom'

    params = {
        'start': start,
        'end': end,
        'air_temp': air_temp,
        'apparent_temp': apparent_temp,
        'cloud': cloud,
        'cloud_type': cloud_type,
        'delta_temp': delta_temp,
        'dew_point': dew_point,
        'time': time,
        'press': press,
        'press_tend': press_tend,
        'rain_trace': rain_trace,
        'vis_km': vis_km,
        'weather': weather,
        'wind_spd_kmh': wind_spd_kmh,
        'size': size,
    }

    bom = requests.get(bom_url, params=params)
    bom_data = bom.json()
    data_bom = [item['_source'] for item in bom_data]
    
    return data_bom

def health(asr=None, disease=None, lga=None, num=None, period=None, phn=None, sr=None, size=2000):

    health_url = 'http://127.0.0.1:9090/health'

    params = {
        'asr': asr,
        'disease': disease,
        'lga': lga,
        'num': num,
        'period': period,
        'phn': phn,
        'sr': sr,
        'size': size,
    }

    health = requests.get(health_url, params=params)
    health_data = health.json()
    data_health = [item['_source'] for item in health_data]
    
    return data_health

def fetch_big_data(total_size, batch_size=10000, source='twitter', **kwargs):
    all_data = []
    fetch_function = {
        'twitter': twitter,
        'bom': bom,
        'epa': epa,
        'health': health,
    }.get(source)
    
    if not fetch_function:
        raise ValueError(f"Invalid source: {source}")
    
    for _ in range(0, total_size, batch_size):
        data = fetch_function(size=batch_size, **kwargs)
        all_data.extend(data)
        print(f"Fetched {len(data)} entries, total so far: {len(all_data)}")
    return all_data

# Example usage:
# fetch_big_data(50000, batch_size=10000, source='twitter')
# fetch_big_data(50000, batch_size=10000, source='bom', start=3)
# fetch_big_data(50000, batch_size=10000, source='epa', city='Melbourne')
# fetch_big_data(50000, batch_size=10000, source='health', disease='COPD')