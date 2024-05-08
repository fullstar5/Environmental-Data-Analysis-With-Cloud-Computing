import json

with open('/mnt/d/ccc_data/Vic_data_v1.json', 'r') as file:
    data = json.load(file)

remaining_data = data[30003:]

new_json_path = '/mnt/d/ccc_data/Vic_data_v3.json'
with open(new_json_path, 'w') as file:
    json.dump(remaining_data, file, ensure_ascii=False, indent=4)

new_json_path

