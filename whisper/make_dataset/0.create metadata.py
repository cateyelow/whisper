import os, sys
from pathlib import Path
import json
from pandas import DataFrame
mp3_directory = 'D:/HuggingFace/datasets/data'
#Load mp3 files in "/data" and make files list
mp3_files_path = 'D:/HuggingFace/KoreanSpeech/mp3_files.txt'
mp3_files = []
if(Path(mp3_files_path).exists()==False):
    for root, dirs, files in os.walk(mp3_directory):
        for file in files:
            if file.endswith('.mp3'):
                mp3_files.append(root + '/' + file)

    #Save mp3_files to txt
    with open(mp3_files_path, 'w', encoding='utf-8-sig') as f:
        for mp3_file in mp3_files:
            f.write(mp3_file + '\n')
else:
    #Load mp3_files
    with open(mp3_files_path, 'r', encoding='utf-8-sig') as f:
        mp3_files = f.read().split('\n')

#replace mp3_files E:/HuggingFace/KoreanSpeech/data/ -> E:/HuggingFace/datasets/data/ 
#mp3_files = [mp3_file.replace('E:/HuggingFace/KoreanSpeech/data/', 'E:/HuggingFace/datasets/data/') for mp3_file in mp3_files] 

json_files_path='D:/HuggingFace/KoreanSpeech/json_files.txt'
json_files = []
no_json_path = 'D:/HuggingFace/invalid_datasets/data'
#Load json files in "/label" which base_name without extension is in mp3_files
if(Path(json_files_path).exists()==False):
    for mp3_file in mp3_files:
        try:
            json_path = Path('D:/HuggingFace/KoreanSpeech/label' + '/' + Path(mp3_file).stem).with_suffix('.json')
            if json_path.exists():
                json_files.append(json_path)
        except:
            print(f'Error: {mp3_file}')
            os.rename(mp3_file, no_json_path + '/' + Path(mp3_file).name)            

    #Save json_files as Path to txt
    with open(json_files_path, 'w', encoding='utf-8-sig') as f:
        for json_file in json_files:
            f.write(str(json_file) + '\n')
else:
    #Load json_files
    with open(json_files_path, 'r', encoding='utf-8-sig') as f:
        json_files = f.read().split('\n')

#Load json data and make metadata which extract "OrgLabelText"  in "전사정보"-> "transcript", metadata is Dataset which column = ['file_name', 'transcript']

print(f'info mp3_files: {len(mp3_files)}')
print(f'info json_files: {len(json_files)}')
#remove all empty string in mp3_files
mp3_files = [mp3_file for mp3_file in mp3_files if mp3_file != '']
#remove all empty string in json_files
json_files = [json_file for json_file in json_files if json_file != '']

# mp3 files which don't have json file move to no_json_path
for mp3_file in mp3_files:
    try:
        if Path('D:/HuggingFace/KoreanSpeech/label' + '/' + Path(mp3_file).stem).with_suffix('.json').exists() == False:
            print(f'No json file: {mp3_file}')
            os.rename(mp3_file, no_json_path + '/' + Path(mp3_file).name)
    except:
            print(f'No json file: {mp3_file}')
            os.rename(mp3_file, no_json_path + '/' + Path(mp3_file).name)
        
metadata = []
for i, json_file in enumerate(json_files):
    try:
        mp3_file_name = Path(json_file).stem + '.mp3'
        with open(json_file, 'r', encoding='utf-8-sig') as f:
            json_data = json.load(f)
            metadata.append([f'data/{mp3_file_name}', json_data['전사정보']['OrgLabelText'].replace(',','')])
    except Exception as e:
        print(e)
        print(f'Error: {json_file}')
        os.rename(mp3_directory + '/' + mp3_file_name, no_json_path + '/' + Path(json_file).stem + '.mp3')


#Save metadata as csv file
df = DataFrame(metadata, columns=['file_name', 'transcription'])
df.to_csv('D:/HuggingFace/KoreanSpeech/metadata.csv', index=False, encoding='utf-8-sig')