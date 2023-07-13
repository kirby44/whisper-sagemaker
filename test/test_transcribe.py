import logging
from unittest.mock import patch
from src import transcribe

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_transcribe():
    logger.info("Starting test: test_transcribe")
    dummy_audio = b"dummy binary data"  # this is now a bytes object, not a BytesIO

    with patch('whisper.transcribe', return_value={"text": "transcribed text"}) as mock_transcribe:
        res = transcribe.TranslateService.transcribe(dummy_audio)
        mock_transcribe.assert_called_once_with(dummy_audio)

        assert res == "transcribed text"
    logger.info('Transcribe function was called correctly with the expected input')

def test_invocations_post():
    logger.info("Starting test: test_invocations_post")
    dummy_transcription = "transcribed text"
    with patch('src.transcribe.TranslateService.transcribe', return_value=dummy_transcription):
        with patch('src.transcribe.base64_to_binary') as mock_b64_to_bin:
            mock_b64_to_bin.return_value = b"dummy binary data"  # this is now a bytes object, not a BytesIO

            with transcribe.app.test_client() as client:
                res = client.post("/invocations", data="dummy base64 data")
                assert res.data.decode('utf-8') == dummy_transcription
                assert res.status_code == 200
    logger.info('Invocations POST endpoint returned expected results')
