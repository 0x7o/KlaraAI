from TTS.api import TTS
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
tts = TTS(model_path="model.pth", config_path="config.json").to("cuda")


@app.get("/tts")
def generate_tts(text: str):
    tts.tts_to_file(text=text, file_path="output.wav", language="ru")
    return FileResponse("output.wav", media_type="audio/wav")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
