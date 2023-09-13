import os
import pathlib

from pathlib import Path
import os
from tqdm import tqdm

#'D:/Datasets_Speech/Korean/014.다화자 음성합성 데이터/01.데이터/1.Training/라벨링데이터/',

def main():
    directory = ['D:/Datasets_Speech/Korean/014.다화자 음성합성 데이터/01.데이터/2.Validation/라벨링데이터/',]
    output_directory = 'D:/HuggingFace/KoreanSpeech/label'
    for d in directory:
        # Recursively search for all WAV files within the directory
        json_files = []
        for root, dirs, files in os.walk(d):
            for file in files:
                #print(file)
                if file.endswith('.json'):
                    json_files.append(Path(root + '/' + file))
                    #print(Path(root + '/' + file))
        #Move JsonFiles
        for json_file in tqdm(json_files):
            try:
                os.rename(json_file, output_directory + '/' + json_file.name)
            except Exception as e:
                print(f'Error: {json_file} {e}')
    
if __name__ == "__main__":
    main()