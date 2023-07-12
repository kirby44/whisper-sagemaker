import base64
from unittest.mock import patch
from src import transcribe

def test_base64_to_wavfile():
    with open('test/base64_audio', 'r') as f:
        base64_audio = f.read().strip()

    with open('test/dialogue1.m4a', 'rb') as f:
        original_audio_data = f.read()

    wav_file = transcribe.base64_to_wavfile(base64_audio)

    assert wav_file.getvalue() == original_audio_data
    print('Base64 decode matched with original audio data correctly')
