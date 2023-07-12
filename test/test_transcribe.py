import unittest
import base64
import os
from src.transcribe import base64_to_wavfile

class TestBase64ToWavfile(unittest.TestCase):
    def test_base64_to_wavfile(self):
        # Read base64 string from file
        with open('test/base64_audio', 'r') as f:
            b64_string = f.read().strip()

        # Read the original audio data
        with open('test/dialogue1.m4a', 'rb') as f:
            original_data = f.read()

        # Call your function with the test data
        result = base64_to_wavfile(b64_string)

        # Check that the returned BytesIO object's content matches the original audio data
        self.assertEqual(result.read(), original_data)

if __name__ == '__main__':
    unittest.main()
