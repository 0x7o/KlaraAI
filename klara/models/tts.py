import io
import wave
import pyaudio
import requests
import numpy as np


class TTS:
    def __init__(self):
        self.endpoint = "http://192.168.0.103:5002/api/tts"
        self.p = pyaudio.PyAudio()

    def play_audio(self, audio_bytes):
        sample_rate = self.get_sample_rate(audio_bytes)
        print(sample_rate)
        stream = self.p.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=sample_rate,
                             output=True)
        audio_array = np.frombuffer(audio_bytes, dtype=np.float32)
        stream.write(audio_array.tobytes())
        stream.stop_stream()
        stream.close()

    def get_sample_rate(self, audio_bytes):
        with io.BytesIO(audio_bytes) as audio_file:
            with wave.open(audio_file, 'rb') as wav_file:
                return wav_file.getframerate()

    def say(self, text):
        response = requests.get(f"{self.endpoint}?text={text}")
        audio_bytes = response.content
        self.play_audio(audio_bytes)

if __name__ == "__main__":
    i = input(">>>")
    tts = TTS()
    tts.say(i)