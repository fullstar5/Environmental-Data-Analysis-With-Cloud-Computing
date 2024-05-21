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

import os
import re
import json

# input_file_path = 'data/twitter-50mb.json'  
# output_file_path = '1Ballarat_data.json'

input_file_path = '/mnt/d/ccc_data/twitter-100gb.json'  
output_file_path = '/mnt/d/ccc_data/Ballarat_data.json' 

pattern = re.compile(rb'"full_name":"[^"]*, Victoria"')

def read_and_filter_tweets(input_path, regex_pattern):

    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            if regex_pattern.search(line.encode('utf-8')):
                yield line.strip()

def write_tweets_in_chunks(filtered_tweets_generator, output_path, chunk_size=10000):

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write('{"rows":[\n')
        first = True  
        tweets_chunk = []
        
        for tweet in filtered_tweets_generator:
            if first:
                tweets_chunk.append(tweet)
                first = False
            else:
                tweets_chunk.append('' + tweet)

            if len(tweets_chunk) >= chunk_size:
                outfile.write("\n".join(tweets_chunk))
                tweets_chunk = []  
        

        if tweets_chunk:
            outfile.write("\n".join(tweets_chunk))
        
        outfile.write("\n{}]}")


filtered_tweets_generator = read_and_filter_tweets(input_file_path, pattern)
write_tweets_in_chunks(filtered_tweets_generator, output_file_path)

print(f"all done in {output_file_path}。")
