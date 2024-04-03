from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

app = FastAPI()

device = "cuda:1" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "distil-whisper/distil-large-v3"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, use_safetensors=True
)
model.config.forced_decoder_ids = AutoProcessor.get_decoder_prompt_ids(language="russian", task="transcribe")
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)

forced_decoder_ids = processor.get_decoder_prompt_ids(language="russian", task="transcribe")

pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    torch_dtype=torch_dtype,
    device=device,
)


class TranscriptionResponse(BaseModel):
    text: str


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    result = pipe(audio_bytes, generate_kwargs={"forced-decoder-ids": forced_decoder_ids})
    return {"text": result["text"]}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
