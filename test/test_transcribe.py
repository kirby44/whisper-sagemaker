import logging
from unittest.mock import patch
from src import transcribe
import io

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_base64_to_wavfile():
    logger.info("Starting test: test_base64_to_wavfile")
    with open('test/base64_audio', 'r') as f:
        base64_audio = f.read().strip()

    with open('test/dialogue1.m4a', 'rb') as f:
        original_audio_data = f.read()

    wav_file = transcribe.base64_to_wavfile(base64_audio)

    assert wav_file.getvalue() == original_audio_data
    logger.info('Base64 decode matched with original audio data correctly')

def test_transcribe():
    logger.info("Starting test: test_transcribe")
    dummy_audio = io.BytesIO(b"dummy binary data")
    dummy_audio.name = "audio.wav"

    with patch('whisper.transcribe.transcribe', return_value={"text": "transcribed text"}) as mock_transcribe:
        res = transcribe.TranslateService.transcribe(dummy_audio)
        mock_transcribe.assert_called_once_with(dummy_audio)

        assert res == "transcribed text"
    logger.info('Transcribe function was called correctly with the expected input')

def test_invocations_post():
    logger.info("Starting test: test_invocations_post")
    dummy_transcription = "transcribed text"
    with patch('src.transcribe.TranslateService.transcribe', return_value=dummy_transcription):
        with patch('src.transcribe.base64_to_wavfile') as mock_b64_to_wav:
            mock_b64_to_wav.return_value = io.BytesIO(b"dummy binary data")

            with transcribe.app.test_client() as client:
                res = client.post("/invocations", data="dummy base64 data")
                assert res.data.decode('utf-8') == dummy_transcription
                assert res.status_code == 200
    logger.info('Invocations POST endpoint returned expected results')
