import numpy as np
import pyaudio
import torch


class VAD:
    def __init__(self, sample_rate=16000, channels=1, format=pyaudio.paInt16, chunk=1024):
        self.model, self.utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                                model='silero_vad',
                                                force_reload=True)
        self.sample_rate = sample_rate
        self.channels = channels
        self.format = format
        self.chunk = chunk
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.voiced_confidences = []

    def int2float(self, audio_int16):
        audio_float32 = audio_int16.astype(np.float32)
        audio_float32 = np.divide(audio_float32, 32768)
        return audio_float32

    def start_recording(self, silence_threshold=0.2, max_silence_duration=1):
        data = []
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.sample_rate,
                                      input=True,
                                      frames_per_buffer=self.chunk,
                                      input_device_index=3)
        silence_duration = 0
        while True:
            audio_chunk = self.stream.read(self.chunk)
            audio_int16 = np.frombuffer(audio_chunk, np.int16)
            audio_float32 = self.int2float(audio_int16)
            data.append(audio_float32)
            new_confidence = self.model(torch.from_numpy(audio_float32), self.sample_rate).item()
            self.voiced_confidences.append(new_confidence)
            if new_confidence < silence_threshold:
                silence_duration += self.chunk / self.sample_rate
            else:
                silence_duration = 0
            if silence_duration >= max_silence_duration:
                break
        return data

    def stop_recording(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
