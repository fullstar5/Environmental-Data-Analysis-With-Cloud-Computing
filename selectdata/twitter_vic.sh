#!/bin/bash

# Elasticsearch API details
URL="https://127.0.0.1:9200/twitter_vic/_doc"
USERNAME="elastic"
PASSWORD="elastic"

# File path
FILE_PATH="/mnt/d/ccc_data/Vic_data_v1.json"

# Read the JSON file and split into individual objects assuming the JSON array structure
jq -c '.[]' $FILE_PATH | while read -r line
do
  # Generate a unique ID for each document using uuidgen, which may require installing the uuid-runtime package
  UUID=$(uuidgen)

  # Use curl to send data to Elasticsearch
  curl -XPUT -k "$URL/$UUID" \
       --header 'Content-Type: application/json' \
       --user "$USERNAME:$PASSWORD" \
       --data "$line" | jq '.'

  # Optional: sleep to prevent overwhelming the server
  # sleep 1
done

