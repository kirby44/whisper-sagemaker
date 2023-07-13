from __future__ import print_function
import os, tempfile
import whisper
import flask
import io
import base64

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")
model_size = "medium"

# TODO: TranscribeService
class TranslateService(object):
    model = None

    @classmethod
    def get_model(cls):
        if cls.model == None:
            cls.model = whisper.load_model(model_size, download_root=model_path)

        return cls.model

    @classmethod
    def transcribe(cls, wav_binary):
        # create a temporary file to store the audio data
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_wav_file:
            temp_wav_file.write(wav_binary)
            temp_wav_file.flush()  # make sure the data is written to disk
            model = cls.get_model()
            res = model.transcribe(temp_wav_file.name)
        return res["text"]


app = flask.Flask(__name__)

@app.route("/ping", methods=["GET"])
def ping():
    health = TranslateService.get_model() is not None

    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")

@app.route("/invocations", methods=["POST"])
def transcribe():
    base64_audio_data = flask.request.get_data().decode("utf-8")
    wav_binary = base64.b64decode(base64_audio_data)
    res = TranslateService.transcribe(wav_binary)
    return flask.Response(response=res, status=200, mimetype="text/plain")
