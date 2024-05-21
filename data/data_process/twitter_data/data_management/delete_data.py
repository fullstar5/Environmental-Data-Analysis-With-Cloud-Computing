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

import json

with open('/mnt/d/ccc_data/Vic_data_v1.json', 'r') as file:
    data = json.load(file)

remaining_data = data[30003:]

new_json_path = '/mnt/d/ccc_data/Vic_data_v3.json'
with open(new_json_path, 'w') as file:
    json.dump(remaining_data, file, ensure_ascii=False, indent=4)

new_json_path

