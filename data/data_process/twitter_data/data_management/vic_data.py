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

import re
import json
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

sentiment_mode = re.compile(rb'"sentiment":(?:(?:{"score":)?([+-]?[0-9]+(?:\.[0-9]+)?))')
full_name_mode = re.compile(rb'"full_name":"([^"]+)"')
text_mode = re.compile(rb'"text":"([^"]+)"')

def process_large_json(file_path, output_filename, block_size=100000, start_index=15001, end_index=50000):
    results = []
    current_block = []
    line_count = 0
    
    with open(file_path, 'rb') as file:
        for line in file:
            line_count += 1
            if line_count > block_size:
                current_block = [] 
                line_count = 1     

            if start_index <= line_count <= end_index:
                current_block.append(line)
                
                if line_count == end_index or (line_count % block_size == 0 and current_block):
                    results.extend(process_block(current_block))
                    current_block = []  

    if current_block:
        results.extend(process_block(current_block))

    with open(output_filename, 'w', encoding='utf-8') as out_file:
        json.dump(results, out_file, indent=4, default=str)

def process_block(block):
    block_results = []
    for line in block:
        sentiment_match = sentiment_mode.search(line)
        full_name_match = full_name_mode.search(line)
        text_match = text_mode.search(line)
        
        if sentiment_match:
            sentiment = float(sentiment_match.group(1).decode('utf-8'))
            full_name = full_name_match.group(1).decode('utf-8').split(',')[0] if full_name_match else 'Unknown'
            text = text_match.group(1).decode('utf-8') if text_match else ''

            try:
                language = detect(text) if text.strip() else 'en'
            except LangDetectException:
                language = 'en'  

            result = {
                'sentiment': sentiment,
                'full_name': full_name,
                'language': language
            }
            block_results.append(result)
    return block_results

input_filename = '/mnt/d/ccc_data/Vic_data.json' 
output_filename = '/mnt/d/ccc_data/Vic_data_v1_1.json'

process_large_json(input_filename, output_filename)
