import base64
from unittest.mock import patch
from src import transcribe

def test_base64_to_wavfile():
    with patch('src.transcribe.whisper') as mock_whisper:
        # create a dummy load_model function
        mock_whisper.load_model.return_value = None

        with open('test/base64_audio', 'r') as f:
            base64_audio = f.read().strip()

        wav_file = transcribe.base64_to_wavfile(base64_audio)

        # Add your assertions here
        assert wav_file is not None
        print(f'wav_file is {wav_file}')  # print information about wav_file
        assert wav_file.name == 'audio.wav'
        print('File name is correct')  # print a success message if the filename assertion passes
        assert wav_file.read() == wav_file.getvalue()
        print('File is base64-encoded correctly')

        assert wav_file.name != 'hoge.wav'

