#!/bin/bash

# Elasticsearch API details
URL="https://127.0.0.1:9200/health_data/_doc"
USERNAME="elastic"
PASSWORD="elastic"

# File path
FILE_PATH="/Users/yueyangwu/Desktop/CCC2/sorted_newData/add_PHN/PM.json"

# Read the JSON file and iterate through each geographical region and period
jq -c '.[] | to_entries[] | .value | to_entries[] | {key, value: .value} | .value | to_entries[] | {key, value: .value}' $FILE_PATH | while read -r entry
do
  # Generate a unique ID for each document using uuidgen, which may require installing the uuid-runtime package
  UUID=$(uuidgen)

  # Extract the key and region data
  region=$(echo $entry | jq -r '.key')
  data=$(echo $entry | jq -r '.value')

  # Use curl to send each entry to Elasticsearch
  curl -XPUT -k "$URL/$UUID" \
       --header 'Content-Type: application/json' \
       --user "$USERNAME:$PASSWORD" \
       --data "$data" | jq '.'

  # Optional: sleep to prevent overwhelming the server
  # sleep 1
done
