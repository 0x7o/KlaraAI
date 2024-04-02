import pyaudio
import torch


class TTS:
    def __init__(self, speaker="kseniya", sample_rate=48000):
        self.model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language="ru",
            speaker="v4_ru",
        )
        self.sample_rate = sample_rate
        self.speaker = speaker
        self.p = pyaudio.PyAudio()

    def play_audio(self, audio):
        audio_np = audio.numpy()  # Convert tensor to numpy array
        stream = self.p.open(
            format=pyaudio.paFloat32, channels=1, rate=self.sample_rate, output=True
        )
        stream.write(audio_np.tobytes())  # Call tobytes on numpy array
        stream.stop_stream()
        stream.close()

    def say(self, text):
        audio = self.model.apply_tts(
            text=text,
            speaker=self.speaker,
            sample_rate=self.sample_rate,
            put_accent=True,
            put_yo=True,
        )
        self.play_audio(audio)
