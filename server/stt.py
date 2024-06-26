from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
from scipy.io import wavfile
import io

app = FastAPI()

device = "cuda:1" if torch.cuda.is_available() else "cpu"

model_id = "lorenzoncina/whisper-small-ru"

model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, use_safetensors=True)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)


class TranscriptionResponse(BaseModel):
    text: str


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    audio_stream = io.BytesIO(audio_bytes)
    sampling_rate, audio_data = wavfile.read(audio_stream)

    input_features = processor(
        audio_data, sampling_rate=sampling_rate, return_tensors="pt"
    ).input_features
    input_features = input_features.to(device)

    predicted_ids = model.generate(input_features, language="ru")

    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return {"text": transcription[0]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
