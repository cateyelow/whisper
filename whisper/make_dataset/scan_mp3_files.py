import os

# Set the directory path
dir_path = "D:/HuggingFace/datasets/data"

# Get a list of all files in the directory
all_files = os.listdir(dir_path)

# Filter the list to only include MP3 files
mp3_files = [f for f in all_files if f.endswith(".mp3")]

# Print the list of MP3 files
print(mp3_files[0:10])

import eyed3
import logging
import io
from pathlib import Path
from tqdm import tqdm
error_path = 'D:/HuggingFace/invalid_datasets/data'

#Load mp3 files using eyed3 and validate
for mp3_file in tqdm(mp3_files):
    log_stream = io.StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)
    mp3_file = dir_path + '/' + mp3_file
    try:
        audiofile = eyed3.load(mp3_file)
        if audiofile == None:
            print(f'Error: {mp3_file}')
            os.rename(mp3_file, error_path + '/' + Path(mp3_file).name)
    except Exception as e:
        print(f'Error: {mp3_file}')
        os.rename(mp3_file, error_path + '/' + Path(mp3_file).name)
    finally:
            # Check log for errors
            log = log_stream.getvalue()
            if "Lame tag CRC check failed" in log:
                print(f'Error: {mp3_file}')
                os.rename(mp3_file, error_path + '/' + Path(mp3_file).name)

import subprocess
import ffmpeg
from concurrent.futures import ProcessPoolExecutor

def is_mp3_broken(mp3_file):
    try:
        probe = ffmpeg.probe(mp3_file)
        return False
    except ffmpeg.Error as e:
        return True

mp3_files = [f for f in os.listdir(dir_path) if f.endswith('.mp3')]

for mp3_file in tqdm(mp3_files):
    mp3_file_path = os.path.join(dir_path, mp3_file)
    if is_mp3_broken(mp3_file_path):
        print(f'오류: {mp3_file}')
        os.rename(mp3_file_path, os.path.join(error_path, Path(mp3_file).name))

#### LIBROSA
