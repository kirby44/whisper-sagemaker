import os
import whisper
import time

audio_dir = './audio/'
language = 'ja'
model_type = 'base'
model = whisper.load_model(model_type)

# Get a list of all audio files in the directory
audio_files = [f for f in os.listdir(audio_dir)]

for audio_file in audio_files:
    audio_path = os.path.join(audio_dir, audio_file)

    start_time = time.time()
    res = model.transcribe(audio_path, language=language)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f'Audio file: {audio_file}')
    print(f'Transcription result: {res}')
    print(f'Time taken to transcribe the audio file: {elapsed_time} seconds')
