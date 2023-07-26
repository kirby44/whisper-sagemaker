import whisper
import time

audio_path = './audio/iPhoneAudio.mp4'
#audio_path = './audio/video.mp4'
#audio_path = './audio/dialogue1.m4a'

language = 'ko'
model_type = 'base'

model = whisper.load_model(model_type)

start_time = time.time()
#res = model.transcribe(audio_path)
res = model.transcribe(audio_path, language=language)
end_time = time.time()
elapsed_time = end_time - start_time

print(f'Transcription result: {res}')
print(f'Time taken to transcribe the audio file: {elapsed_time} seconds')