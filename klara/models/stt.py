import io
import requests
import numpy as np
from scipy.io import wavfile


class STT:
    def __init__(self, server_url="http://192.168.0.103:8000"):
        self.server_url = server_url

    def process(self, audio, sample_rate=16000):
        audio_floats = np.concatenate(
            [np.frombuffer(a, dtype=np.float32) for a in audio]
        )
        audio_int16 = (audio_floats * 32767).astype(np.int16)

        audio_bytes = io.BytesIO()
        wavfile.write(audio_bytes, sample_rate, audio_int16)
        audio_bytes.seek(0)

        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        response = requests.post(f"{self.server_url}/transcribe", files=files)

        if response.status_code == 200:
            transcription = response.json()["text"]
            return transcription
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")
