import logging
import base64
import unittest
from unittest.mock import patch, ANY, Mock
from src import transcribe
import pytest
import unittest

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TestTranscribe(unittest.TestCase):
    def setUp(self):
        self.audio_binary_wav = b'RIFF' + b'a' * 100
        self.audio_binary_mp3 = b'ID3' + b'a' * 100
        self.audio_binary_m4a = b'\x00\x00\x00\x20ftypM4A ' + b'a' * 100
        self.audio_binary_mp4 = b'\x00\x00\x00\x18ftypisom' + b'a' * 100
        self.audio_binary_webm = b'\x1a\x45\xdf\xa3' + b'a' * 100
        self.audio_binary_mpeg = b'\x00\x00\x01\xba' + b'a' * 100
        self.audio_binary_mpga = b'\xFF\xF3' + b'a' * 100

    def test_get_file_extension_from_binary(self):
        self.assertEqual(transcribe.TranslateService.get_file_extension_from_binary(self.audio_binary_wav), '.wav')
        self.assertEqual(transcribe.TranslateService.get_file_extension_from_binary(self.audio_binary_mp3), '.mp3')
        self.assertEqual(transcribe.TranslateService.get_file_extension_from_binary(self.audio_binary_m4a), '.m4a')
        self.assertEqual(transcribe.TranslateService.get_file_extension_from_binary(self.audio_binary_mp4), '.mp4')
        self.assertEqual(transcribe.TranslateService.get_file_extension_from_binary(self.audio_binary_webm), '.webm')
        self.assertEqual(transcribe.TranslateService.get_file_extension_from_binary(self.audio_binary_mpeg), '.mpeg')
        self.assertEqual(transcribe.TranslateService.get_file_extension_from_binary(self.audio_binary_mpga), '.mpga')

    def test_transcribe_with_different_file_types(self):
        logger.info("Starting test: test_transcribe_with_different_file_types")
        dummy_model = Mock()  # create a dummy model
        dummy_model.transcribe.return_value = {"text": "transcribed text"}

        # Replace whisper.load_model with a function that returns the dummy model
        with patch('whisper.load_model', return_value=dummy_model):
            # Test with all supported file types
            #for binary in [self.audio_binary_wav, self.audio_binary_mp3, self.audio_binary_m4a, self.audio_binary_webm, self.audio_binary_mpeg, self.audio_binary_mpga]:
            for binary in [self.audio_binary_wav, self.audio_binary_mp3, self.audio_binary_m4a, self.audio_binary_mp4, self.audio_binary_webm, self.audio_binary_mpeg, self.audio_binary_mpga]:
                res = transcribe.TranslateService.transcribe(binary)
                dummy_model.transcribe.assert_called()  # Check that the dummy model was used
                assert res == "transcribed text"

            # Clean up after the test
            transcribe.TranslateService.model = None

        logger.info('Transcribe function was called correctly with different file types')

if __name__ == "__main__":
    unittest.main()
