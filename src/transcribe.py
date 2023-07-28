from __future__ import print_function
import os, tempfile
import whisper
import flask
import sys
import base64
import boto3
from pydub import AudioSegment

# for test purpose, can be removed safely if not needed
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add stdout handler, to make sure not to be captured by Flask and won't be shown in CloudWatch
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")
model_size = "base"

# TODO: TranscribeService
class TranslateService(object):
    model = None

    @classmethod
    def get_model(cls):
        if cls.model == None:
            cls.model = whisper.load_model(model_size, download_root=model_path)

        return cls.model

    @classmethod
    def get_file_extension_from_binary(cls, binary):
        # check for various file signatures
        if binary.startswith(b'RIFF'):
            return '.wav'
        elif binary.startswith(b'ID3') or binary.startswith(b'\xFF\xFB'):
            return '.mp3'
        elif binary[4:4+8] == b'ftypM4A ':
            return '.m4a'
        elif binary[4:4+8] in [b'ftypisom', b'ftypmp42', b'ftypiso5', b'ftypiso6', b'ftypM4V ', b'ftypqt  ']:
            return '.mp4'
        elif binary.startswith(b'\x1a\x45\xdf\xa3'):
            return '.webm'
        elif binary.startswith(b'\x00\x00\x01\xba') or binary.startswith(b'\x00\x00\x01\xb3'):
            return '.mpeg'
        elif binary.startswith(b'\xFF\xF3') or binary.startswith(b'\xFF\xFA'):
            return '.mpga'
        else:
            return '.mp4'  

    @classmethod
    def transcribe(cls, audio_binary, *, initial_prompt=None, language='ja'):
        # add logging
        logger.info("In transcribe method. Language: {}, initial_prompt: {}".format(language, initial_prompt))

        file_extension = cls.get_file_extension_from_binary(audio_binary)
        logger.info(f'file extension: {file_extension}')

        # create a temporary file to store the audio data
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_audio_file:
            temp_audio_file.write(audio_binary)
            temp_audio_file.flush()  # make sure the data is written to disk
            model = cls.get_model()

            # add logging
            logger.info("Model obtained: {}".format(model))

            # Upload the file to S3
            s3_client = boto3.client('s3')
            s3_bucket = "sagemaker-ap-northeast-1-133132895539"
            s3_key = f"whisper/beforetranscribed/{os.path.basename(temp_audio_file.name)}"
            s3_client.upload_file(temp_audio_file.name, s3_bucket, s3_key)
            logger.info(f"File uploaded to S3: {s3_bucket}/{s3_key}")

            # Pass initial_prompt to the transcribe method
            res = model.transcribe(temp_audio_file.name, initial_prompt=initial_prompt, language=language)

            # add logging
            logger.info("Result: {}".format(res))
            logger.info(f"transcription: {res['text']}")

        return res["text"]

app = flask.Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    health = TranslateService.get_model() is not None

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")

@app.route("/invocations", methods=["POST"])
def transcribe():
    data = flask.request.get_json()  # assumes that incoming request data is a JSON object
    logger.info(f'data: {data}')
    base64_audio_data = data['audio']  
    logger.info(f'audio: {base64_audio_data}')
    initial_prompt = data.get('initial_prompt')  # get 'initial_prompt' from the request, if it exists
    language = data.get('language')
    audio_binary = base64.b64decode(base64_audio_data)
    res = TranslateService.transcribe(audio_binary, initial_prompt = initial_prompt, language = language)
    return flask.Response(response=res, status=200, mimetype="text/plain")
