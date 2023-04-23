from transformers import pipeline
import whisper
import gradio as gr
import time
pipe = pipeline(model="trueorfalse441/whisper-small-ko", chunk_length_s=30, device=0)  # change to "your-username/the-name-you-picked"

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("audio.m4a")
#audio = whisper.pad_or_trim(audio)
start = time.time()
pipe(audio)
end = time.time() - start
print(f'elapsed time : {end}')

