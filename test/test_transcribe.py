import logging
import base64
from unittest.mock import patch, ANY, Mock
from src import transcribe

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def test_transcribe():
    logger.info("Starting test: test_transcribe")
    dummy_audio = b"dummy binary data"  # this is now a bytes object

    dummy_model = Mock()  # create a dummy model
    dummy_model.transcribe.return_value = {"text": "transcribed text"}

    # Replace whisper.load_model with a function that returns the dummy model
    with patch('whisper.load_model', return_value=dummy_model):
        res = transcribe.TranslateService.transcribe(dummy_audio)

        dummy_model.transcribe.assert_called_once_with(ANY)  # Check that the dummy model was used

        assert res == "transcribed text"
    logger.info('Transcribe function was called correctly with the expected input')


def test_invocations_post():
    logger.info("Starting test: test_invocations_post")
    dummy_transcription = "transcribed text"
    with patch('src.transcribe.TranslateService.transcribe', return_value=dummy_transcription):
        with transcribe.app.test_client() as client:
            res = client.post("/invocations", data=base64.b64encode(b"dummy binary data").decode("utf-8"))
            assert res.data.decode('utf-8') == dummy_transcription
            assert res.status_code == 200
    logger.info('Invocations POST endpoint returned expected results')
