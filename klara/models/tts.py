import io
import wave
import pyaudio
import aiohttp
import asyncio
import numpy as np


class TTS:
    def __init__(self):
        self.endpoint = "http://192.168.0.103:5002/api/tts"
        self.p = pyaudio.PyAudio()

    async def play_audio(self, audio_bytes):
        sample_rate = self.get_sample_rate(audio_bytes)
        stream = self.p.open(format=pyaudio.paInt16,
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

    async def get_audio(self, text):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.endpoint}?text={text}") as response:
                return await response.read()

    async def say_async(self, text_list):
        audio_bytes = await self.get_audio(text_list[0])
        play_task = asyncio.create_task(self.play_audio(audio_bytes))

        for text in text_list[1:]:
            audio_bytes = await self.get_audio(text)
            await play_task
            play_task = asyncio.create_task(self.play_audio(audio_bytes))

        await play_task

    def say(self, text_list):
        asyncio.run(self.say_async(text_list))