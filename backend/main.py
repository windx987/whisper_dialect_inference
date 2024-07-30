from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File
import base64

app = FastAPI()

import torch
from transformers import (pipeline,
                          WhisperFeatureExtractor, 
                          WhisperTokenizer, 
                          WhisperProcessor, 
                          WhisperForConditionalGeneration)

MODEL_NAME = 'biodatlab/whisper-th-medium-combined'
PATH = './model.pth'

model = WhisperForConditionalGeneration.from_pretrained(MODEL_NAME)
model.generation_config.language = "Thai"
model.generation_config.task = "transcribe"
model.generation_config.forced_decoder_ids = None
model.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')))

tokenizer = WhisperTokenizer.from_pretrained(MODEL_NAME)
feature_extractor = WhisperFeatureExtractor.from_pretrained(MODEL_NAME)

# Move the model to the specified device
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Create a pipeline for automatic speech recognition
pipe = pipeline(
    "automatic-speech-recognition", 
    model=model, 
    tokenizer=tokenizer, 
    feature_extractor=feature_extractor,
    device=0 if device == "cuda" else -1
)

@app.get("/")
async def root():
    return {"message": "API is up and running!", "status": "ok"}

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    try:
        audio_bytes = await file.read()
        transcription = pipe(audio_bytes)
        return JSONResponse(content=transcription['text'])
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)