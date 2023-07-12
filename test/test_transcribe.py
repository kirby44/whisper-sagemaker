import unittest
import base64
from unittest.mock import patch

class TestTranscribe(unittest.TestCase):
    @patch('src_tmp.transcribe.whisper')
    def test_base64_to_wavfile(self, mock_whisper):
        # create a dummy load_model function
        mock_whisper.load_model.return_value = None

        import transcribe
        with open('test/base64_audio', 'r') as f:
            base64_audio = f.read().strip()

        wav_file = transcribe.base64_to_wavfile(base64_audio)

        # Add your assertions here
        self.assertIsNotNone(wav_file)
        print(f'wav_file is {wav_file}')  # print information about wav_file
        self.assertEqual(wav_file.name, 'audio.wav')
        print('File name is correct')  # print a success message if the filename assertion passes
        self.assertEqual(wav_file.read(), wav_file)
        print('File is base64-encoded correctly')

        self.assertEqual(wav_file.name, 'hoge.wav')
 

if __name__ == '__main__':
    unittest.main()
