import pyaudio
import requests
import numpy as np


class TTS:
    def __init__(self, sample_rate=44100):
        self.endpoint = "http://192.168.0.111:8000/tts"
        self.sample_rate = sample_rate
        self.p = pyaudio.PyAudio()

    def play_audio(self, audio_bytes):
        audio_np = np.frombuffer(audio_bytes, dtype=np.float32)
        stream = self.p.open(
            format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, output=True
        )
        stream.write(audio_np.tobytes())
        stream.stop_stream()
        stream.close()

    def say(self, text):
        response = requests.get(f"{self.endpoint}?text={text}")
        audio_bytes = response.content
        self.play_audio(audio_bytes)
