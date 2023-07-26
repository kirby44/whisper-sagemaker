import logging
import base64
import unittest
from unittest.mock import patch, Mock, ANY, mock_open
import pytest
from src import transcribe

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@pytest.fixture
def mock_transcribe_setup():
    with patch('tempfile.NamedTemporaryFile', return_value=mock_open(read_data=b'dummy binary data')()) as mocked_temp_file, \
         patch('whisper.load_model', return_value=Mock()), \
         patch('boto3.client', return_value=Mock()), \
         patch('os.path.splitext', return_value=['/tmp/tmpsr98x98o', '.wav']), \
         patch('os.path.basename', return_value='tmpsr98x98o.wav'), \
         patch('src.transcribe.AudioSegment.from_file', return_value=Mock()), \
         patch('builtins.open', mock_open(read_data=b'dummy binary data')):
        yield mocked_temp_file

def test_transcribe(mock_transcribe_setup):
    logger.info("Starting test: test_transcribe")
    dummy_audio = b"dummy binary data"  # this is now a bytes object

    res = transcribe.TranslateService.transcribe(dummy_audio)

    assert res == "transcribed text"

def test_transcribe_initial_prompt(mock_transcribe_setup):
    logger.info("Starting test: test_transcribe_initial_prompt")
    dummy_audio = b"dummy binary data"  # this is now a bytes object
    dummy_initial_prompt = "initial_prompt"

    res = transcribe.TranslateService.transcribe(dummy_audio, initial_prompt=dummy_initial_prompt)

    assert res == "transcribed text"

def test_invocations_post(mock_transcribe_setup):
    logger.info("Starting test: test_invocations_post")
    dummy_transcription = "transcribed text"
    request_data = {
        "audio": base64.b64encode(b"dummy binary data").decode("utf-8"),
    }

    with patch('src.transcribe.TranslateService.transcribe', return_value=dummy_transcription) as mocked_transcribe:
        with transcribe.app.test_client() as client:
            res = client.post("/invocations", json=request_data)
            assert res.data.decode('utf-8') == dummy_transcription
            assert res.status_code == 200
            mocked_transcribe.assert_called_once_with(ANY, language=None, initial_prompt=None)

def test_invocations_post_with_initial_prompt(mock_transcribe_setup):
    logger.info("Starting test: test_invocations_post_with_initial_prompt")
    dummy_transcription = "transcribed text"
    dummy_initial_prompt = "initial_prompt"
    request_data = {
        "audio": base64.b64encode(b"dummy binary data").decode("utf-8"),
        "initial_prompt": dummy_initial_prompt
    }

    with patch('src.transcribe.TranslateService.transcribe', return_value=dummy_transcription) as mocked_transcribe:
        with transcribe.app.test_client() as client:
            res = client.post("/invocations", json=request_data)
            assert res.data.decode('utf-8') == dummy_transcription
            assert res.status_code == 200
            mocked_transcribe.assert_called_once_with(ANY, language=None, initial_prompt=dummy_initial_prompt)

@pytest.mark.parametrize("language, expected_language", [
    (None, 'ja'),  # language in request is not defined, so it should default to 'ja'
    ('ja', 'ja'),  # language = 'ja'
    ('en', 'en'),  # language = 'en'
    ('xx', 'xx'),  # language = 'xx', even though it's invalid, the function should still pass it through
])
def test_transcribe_different_languages(language, expected_language, mock_transcribe_setup):  # Use the fixture here
    logger.info(f"Starting test: test_transcribe_different_languages with language={language}")
    dummy_audio = b"dummy binary data"  # this is now a bytes object

    if language is None:
        res = transcribe.TranslateService.transcribe(dummy_audio)
    else:
        res = transcribe.TranslateService.transcribe(dummy_audio, language=language)

    assert res == "transcribed text"
