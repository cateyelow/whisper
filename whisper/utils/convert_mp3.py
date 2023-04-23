import os
import pathlib
from concurrent.futures import as_completed, ThreadPoolExecutor
from multiprocessing import cpu_count, Pool
from zipfile import ZipFile


#from keras.utils import get_file
from pydub import AudioSegment, effects
from tqdm import tqdm

from pathlib import Path
import os

# def download_archive(url):
#     filename = os.path.split(url)[-1]
#     try:
#         filename = get_file(fname=filename, origin=url, cache_dir="./", extract=False)
#     except:
#         print(f"Unable to download {url}")
#         return None
#     return filename

def extract_zipfile(filename):
    filename = pathlib.Path(filename)
    dirname = filename.parent / filename.stem
    with ZipFile(filename, "r") as zipf:
        for zipinfo in zipf.infolist():
            if zipinfo.filename[-1] == "/":
                continue
            zipinfo.filename = pathlib.Path(zipinfo.filename).name
            if pathlib.Path(zipinfo.filename).suffix == ".wav":
                zipf.extract(zipinfo, dirname / "wav")
            else:
                zipf.extract(zipinfo, dirname)
    wavfiles = list((dirname / "wav").rglob("*.wav"))
    return wavfiles




def get_mp3_path(wavfile):
    mp3dir = list(wavfile.parents)[1] / "mp3"
    mp3dir.mkdir(parents=True, exist_ok=True)
    mp3file = mp3dir / wavfile.with_suffix(".mp3").name
    return mp3file




def convert_wav_to_mp3(wavfile, output):
    mp3file = Path(output + wavfile.stem + ".mp3")
    print(mp3file)
    #Check mp3 file already exists
    if mp3file.exists():
        print(mp3file.stem + " already exists")
        return mp3file
    try:
        wavaudio = AudioSegment.from_wav(wavfile)
        wavaudio = wavaudio.set_frame_rate(16000).set_channels(1)
        wavaudio = effects.normalize(wavaudio)
        wavaudio.export(mp3file, format="mp3", bitrate="16k")
        print(mp3file.stem + " converted to mp3")
        return mp3file
    except Exception as e:
        print(f"Unable to convert {wavfile} to mp3")
        print(e)





def main():
    directory = 'E:/Datasets_Speech/Korean/014.다화자 음성합성 데이터/01.데이터/1.Training/원천데이터/'
    output_directory = 'E:/Datasets_Speech/Korean/014.다화자 음성합성 데이터/01.데이터/1.Training/원천데이터/converted/'
    # Recursively search for all WAV files within the directory
    wav_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            if file.endswith('.wav'):
                wav_files.append(Path(root + '/' + file))
                print(Path(root + '/' + file))
    # convert wav to mp3 in wav_files
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        futures = [executor.submit(convert_wav_to_mp3, Path(wavfile), output_directory) for wavfile in wav_files]
        for future in tqdm(as_completed(futures), total=len(futures)):
            pass
    
    



if __name__ == "__main__":
    main()
