import aiohttp
import asyncio
import tempfile
import os


class TTS:
    def __init__(self):
        self.endpoint = "http://192.168.0.103:5002/api/tts"

    async def play_audio(self, file_name):
        command = f"aplay -D plughw:3,0 {file_name}"
        process = await asyncio.create_subprocess_shell(command)
        await process.wait()

        os.unlink(file_name)

    async def get_audio(self, text):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.endpoint}?text={text}") as response:
                bytes = await response.read()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    temp_file.write(bytes)
                    return temp_file.name

    async def say_async(self, text_list):
        file_name = await self.get_audio(text_list[0])
        play_task = asyncio.create_task(self.play_audio(file_name))

        for text in text_list[1:]:
            file_name = await self.get_audio(text)
            await play_task
            play_task = asyncio.create_task(self.play_audio(file_name))

        await play_task

    def say(self, text_list):
        asyncio.run(self.say_async(text_list))
