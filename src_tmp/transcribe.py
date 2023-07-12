from __future__ import print_function
import os, tempfile
import whisper
import flask
import io
import base64

prefix = "/opt/ml/"
model_path = os.path.join(prefix, "model")
model_size = "medium"

def base64_to_wavfile(wav_base64) -> io.BytesIO:
    wav_binary = base64.b64decode(wav_base64)
    wav_file = io.BytesIO(wav_binary)
    wav_file.name = "audio.wav"
    return wav_file

# TODO: TranscribeService
class TranslateService(object):
    model = None

    @classmethod
    def get_model(cls):
        if cls.model == None:
            cls.model = whisper.load_model(model_size, download_root=model_path)

        return cls.model

    @classmethod
    def transcribe(cls, voice_file):
        model = cls.get_model()
        res = model.transcribe(voice_file)

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
    wav_file = base64_to_wavfile(base64_audio_data)
    res = TranslateService.transcribe(wav_file)
    return flask.Response(response=res, status=200, mimetype="text/plain")
