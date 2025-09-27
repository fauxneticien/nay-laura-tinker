from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
import os

import torch

torch.set_num_threads(1)

vad_model, (get_speech_timestamps, _, read_audio, _, _) = torch.hub.load(
    repo_or_dir='/silero-vad',
    source='local',
    model='silero_vad',
    verbose=False
)

app = FastAPI()

# Mount templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-audio/")
async def upload_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        return JSONResponse(content={"error": "Invalid file type"}, status_code=400)

    # Read file into memory
    contents = await file.read()

    file_ext  = os.path.splitext(file.filename)[1]  # e.g., '.mp3'
    file_path = "/tmp/audio" + file_ext

    # Write out to disk, since read_audio() expects a file path
    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        audio = read_audio(file_path)

        timestamps = get_speech_timestamps(
            audio,
            vad_model,
            min_speech_duration_ms=500,
            max_speech_duration_s=20,
            min_silence_duration_ms=750,
            # Important, use return_seconds=True for post-vad merge function
            return_seconds=True
        )

        return {
            "timestamps": timestamps
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
