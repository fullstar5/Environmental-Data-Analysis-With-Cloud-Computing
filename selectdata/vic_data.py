#select the re part from the origin json file
import re
import json
from datetime import datetime
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Regex patterns to extract data from JSON strings
time_mode = re.compile(rb'"created_at":"([^"]+)"')
sentiment_mode = re.compile(rb'"sentiment":(?:(?:{"score":)?([+-]?[0-9]+(?:\.[0-9]+)?))')
full_name_mode = re.compile(rb'"full_name":"([^"]+)"')
text_mode = re.compile(rb'"text":"([^"]+)"')

def process_large_json(file_path, output_filename, block_size=100000, process_limit=15000):
    results = []
    current_block = []
    line_count = 0
    
    with open(file_path, 'rb') as file:
        for line in file:
            line_count += 1
            if line_count > block_size:
                current_block = []  # Reset block
                line_count = 1     # Reset line counter

            if line_count <= process_limit:
                current_block.append(line)
                
                # Process the block if it reaches the process limit
                if line_count == process_limit:
                    results.extend(process_block(current_block))
    
    # Final block processing if it didn't reach the full limit
    if current_block:
        results.extend(process_block(current_block))

    with open(output_filename, 'w', encoding='utf-8') as out_file:
        json.dump(results, out_file, indent=4, default=str)

def process_block(block):
    block_results = []
    for line in block:
        time_match = time_mode.search(line)
        sentiment_match = sentiment_mode.search(line)
        full_name_match = full_name_mode.search(line)
        text_match = text_mode.search(line)
        
        if time_match and sentiment_match:
            created_at = time_match.group(1).decode('utf-8')
            sentiment = float(sentiment_match.group(1).decode('utf-8'))
            full_name = full_name_match.group(1).decode('utf-8').split(',')[0] if full_name_match else 'Unknown'
            text = text_match.group(1).decode('utf-8') if text_match else ''

            try:
                language = detect(text) if text.strip() else 'en'
            except LangDetectException:
                language = 'en'  

            dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))

            result = {
                # 'created_at': dt.strftime('%Y-%m-%d %H:%M:%S'),
                'sentiment': sentiment,
                'full_name': full_name,
                'language': language
            }
            block_results.append(result)
    return block_results


input_filename = '/mnt/d/ccc_data/Vic_data.json' 
output_filename = '/mnt/d/ccc_data/Vic_data_v1.json'

# input_filename = 'selectdata/sample.json' 
# output_filename = 'selectdata/output.json'

process_large_json(input_filename, output_filename)
