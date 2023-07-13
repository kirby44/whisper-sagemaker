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

        dummy_model.transcribe.assert_called_once()  # Check that the dummy model was used

        assert res == "transcribed text"

        # Clean up after the test
        transcribe.TranslateService.model = None

    logger.info('Transcribe function was called correctly with the expected input')

def test_transcribe_initial_prompt():
    logger.info("Starting test: test_transcribe_initial_prompt")
    dummy_audio = b"dummy binary data"  # this is now a bytes object
    dummy_initial_prompt = "initial_prompt"

    dummy_model = Mock()  # create a dummy model
    dummy_model.transcribe.return_value = {"text": "transcribed text"}

    # Replace whisper.load_model with a function that returns the dummy model
    with patch('whisper.load_model', return_value=dummy_model):
        # Add the initial_prompt argument when calling the transcribe method
        res = transcribe.TranslateService.transcribe(dummy_audio, initial_prompt=dummy_initial_prompt)

        # Check that the dummy model was used with the correct arguments
        dummy_model.transcribe.assert_called_once()


        assert res == "transcribed text"
    logger.info('Transcribe function was called correctly with the expected initial_prompt')

def test_invocations_post():
    logger.info("Starting test: test_invocations_post")
    dummy_transcription = "transcribed text"
    with patch('src.transcribe.TranslateService.transcribe', return_value=dummy_transcription):
        with transcribe.app.test_client() as client:
            res = client.post("/invocations", data=base64.b64encode(b"dummy binary data").decode("utf-8"))
            assert res.data.decode('utf-8') == dummy_transcription
            assert res.status_code == 200
    logger.info('Invocations POST endpoint returned expected results')
