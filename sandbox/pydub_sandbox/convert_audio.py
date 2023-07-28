from pydub import AudioSegment
import os

# Load audio file
audio = AudioSegment.from_file("audio/iPhoneAudioSafari.mp4", format="mp4")

# Export as .wav
audio.export("sandbox/pydub_sandbox/output.wav", format="wav")
