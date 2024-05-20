#format json file to match with bulk api
import json

# Load the original data
with open('/mnt/d/ccc_data/Vic_data_v1_1.json', 'r') as file:
    data = json.load(file)

# Create the new list with the index lines
new_data = []
for entry in data:
    new_data.append({"index": {"_index": "twitter_vic", "_type": "_doc"}})
    new_data.append(entry)

# Write the new data to a new JSON file
with open('/mnt/d/ccc_data/vic_data_v2_2.json', 'w') as file:
    for item in new_data:
        json.dump(item, file)
        file.write('\n')  

