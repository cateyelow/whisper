import os

# Set the directory path
dir_path = "D:/HuggingFace/datasets/data"

# Get a list of all files in the directory
all_files = os.listdir(dir_path)

# Filter the list to only include MP3 files
mp3_files = [f for f in all_files if f.endswith(".mp3")]

from pathlib import Path
from tqdm import tqdm
error_path = 'D:/HuggingFace/invalid_datasets/data'

from concurrent.futures import ProcessPoolExecutor

import os
import librosa
from tqdm import tqdm

def is_mp3_broken(mp3_file):
    try:
        y, sr = librosa.load(mp3_file)
        return False
    except Exception as e:
        return True

mp3_files = [f for f in os.listdir(dir_path) if f.endswith('.mp3')]
for mp3_file in tqdm(mp3_files):
    mp3_file_path = os.path.join(dir_path, mp3_file)
    if is_mp3_broken(mp3_file_path):
        print(f'오류: {mp3_file}')
        os.rename(mp3_file_path, os.path.join(error_path, Path(mp3_file).name))


#### LIBROSA
