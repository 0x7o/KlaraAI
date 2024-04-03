import pyaudio
import requests
import numpy as np


class TTS:
    def __init__(self):
        self.endpoint = "http://192.168.0.103:5002/api/tts"
        self.p = pyaudio.PyAudio()

    def play_audio(self, audio_bytes):
        stream = self.p.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=44100,
                             output=True)
        audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
        stream.write(audio_array.tobytes())
        stream.stop_stream()
        stream.close()

    def say(self, text):
        response = requests.get(f"{self.endpoint}?text={text}")
        audio_bytes = response.content
        self.play_audio(audio_bytes)
