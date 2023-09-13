import os
import pathlib

from pathlib import Path
import os
from tqdm import tqdm

def main():
    directory = ['D:/Datasets_Speech/Korean/014.다화자 음성합성 데이터/01.데이터/1.Training/원천데이터/converted',
                    'D:/Datasets_Speech/Korean/014.다화자 음성합성 데이터/01.데이터/2.Validation/원천데이터/converted',]
    output_directory = 'D:/HuggingFace/datasets/data'
    for d in directory:
        # Recursively search for all WAV files within the directory
        mp3_files = []
        for root, dirs, files in os.walk(d):
            for file in files:
                #print(file)
                if file.endswith('.mp3'):
                    mp3_files.append(Path(root + '/' + file))
                    #print(Path(root + '/' + file))
        #Move JsonFiles
        for json_file in tqdm(mp3_files):
            try:
                os.rename(json_file, output_directory + '/' + json_file.name)
            except:
                #print(f'Error: {json_file}')
                pass
    
if __name__ == "__main__":
    main()