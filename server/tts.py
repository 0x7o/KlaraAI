from TTS.api import TTS
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
tts = TTS("klara-tts/").to("cuda:0")


@app.get("/tts")
def generate_tts(text: str):
    tts.tts_to_file(text=text, file_path="output.wav")
    return FileResponse("output.wav", media_type="audio/wav")
