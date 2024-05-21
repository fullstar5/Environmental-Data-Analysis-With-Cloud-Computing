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

# format json file to match with bulk api
import json

with open('/mnt/d/ccc_data/Vic_data_v1_1.json', 'r') as file:
    data = json.load(file)

new_data = []
for entry in data:
    new_data.append({"index": {"_index": "twitter_vic", "_type": "_doc"}})
    new_data.append(entry)

with open('/mnt/d/ccc_data/vic_data_v2_2.json', 'w') as file:
    for item in new_data:
        json.dump(item, file)
        file.write('\n')  
