from huggingface_hub import HfApi

# Replace 'your_api_token' with the actual API token you generated from Hugging Face website
api_token = "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"

# Authenticate using the API token
hf_api = HfApi()
user_info = hf_api.whoami(token=api_token)

# Select CUDA device index
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
model_name_or_path = "openai/whisper-large-v2"
#model_name_or_path = "E:/whisper/whisper/whisper/whisper-large-v2-100h/checkpoint-17500/adapter_model"
language = "Korean"
language_abbr = "ko"
task = "transcribe"

from datasets import load_dataset
dataset_test = load_dataset("trueorfalse441/korean-speach-5000-hour")

dataset = dataset_test

#Load FreatureExtractor
from transformers import WhisperFeatureExtractor
#Load WhisperTokenizer
from transformers import WhisperTokenizer

feature_extractor = WhisperFeatureExtractor.from_pretrained("openai/whisper-large-v2")
tokenizer = WhisperTokenizer.from_pretrained("openai/whisper-large-v2", language="Korean", task="transcribe")

#Sharding dataset
total_size_train = len(dataset['train'])
datasets = []
for i in range(100):
    datasets.append(dataset['train'].shard(num_shards=100, index=i))

#Prepare Dataset
def prepare_dataset(batch, feature_extractor=feature_extractor, tokenizer=tokenizer) :
    # load and resample audio data from 48 to 16kHz
    audio = batch["audio"]

    # compute log-Mel input features from input audio array 
    batch["input_features"] = feature_extractor(audio["array"], sampling_rate=audio["sampling_rate"]).input_features[0]

    # encode target text to label ids 
    batch["labels"] = tokenizer(batch["transcription"]).input_ids
    return batch

#Verify Tokenizer
input_str = dataset['train'][0]['transcription']
labels = tokenizer(input_str).input_ids
decoded_with_special = tokenizer.decode(labels, skip_special_tokens=False)
decoded_str = tokenizer.decode(labels, skip_special_tokens=True)

print(f"Input:                 {input_str}")
print(f"Decoded w/ special:    {decoded_with_special}")
print(f"Decoded w/out special: {decoded_str}")
print(f"Are equal:             {input_str == decoded_str}")

#Combine To Create A WhisperProcessor
from transformers import WhisperProcessor
processor = WhisperProcessor.from_pretrained("openai/whisper-large", language="Korean", task="transcribe")

#ReSampling
from datasets import Audio
import multiprocessing
# dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))

import os
import glob

def delete_cache_files(directory):
    # Construct the pattern to match all files starting with 'cache'
    pattern = os.path.join(directory, '**', 'cache*')
    
    # Use glob to find all files matching the pattern, recursively
    files_to_delete = glob.glob(pattern, recursive=True)
    
    # Iterate over the list of files to delete
    for file in files_to_delete:
        try:
            # Check if it's a file and not a directory
            if os.path.isfile(file):
                # Delete the file
                os.remove(file)
                print(f"Deleted: {file}")
            else:
                print(f"Skipped (not a file): {file}")
        except Exception as e:
            # Print any errors encountered during the file deletion
            print(f"Error deleting {file}: {e}")

# Call the function with the path to the .cache directory
delete_cache_files(r"E:\.cache")


for i, dataset in enumerate(datasets):
    if os.path.exists(f"whisper-5000/{i}"):
        continue

    print(f"{i}/{len(datasets)}: {dataset}")
    dataset = dataset.map(prepare_dataset, 
                                remove_columns=dataset.column_names, num_proc=16,
                                fn_kwargs={"feature_extractor": feature_extractor, "tokenizer": tokenizer},   
                                load_from_cache_file=False,     
                                writer_batch_size=6000,#batched=True,
                                )
    if not os.path.exists(f"whisper-5000/{i}"):
        os.makedirs(f"whisper-5000/{i}")

    datasets[i].save_to_disk(f"whisper-5000/{i}")

    #delete cache file
    delete_cache_files(r"E:\.cache")