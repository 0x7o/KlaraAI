import io
import wave
import aiohttp
import asyncio
import numpy as np
import tempfile
import os


class TTS:
    def __init__(self):
        self.endpoint = "http://192.168.0.103:5002/api/tts"

    async def play_audio(self, audio_bytes):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name

        command = f"aplay -D plughw:1,0 {temp_file_path}"
        process = await asyncio.create_subprocess_shell(command)
        await process.wait()

        os.unlink(temp_file_path)

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

if __name__ == "__main__":
    texts = ["И смех, и грех лопашыващывапвыал" for i in range(10)]
    tts = TTS()
    tts.say(texts)