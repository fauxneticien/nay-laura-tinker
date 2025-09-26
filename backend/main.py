from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydub import AudioSegment
import io
import time

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

    try:
        # Use pydub to load audio
        audio = AudioSegment.from_file(io.BytesIO(contents))
        duration_seconds = round(len(audio) / 1000, 2)
        frame_rate = audio.frame_rate
        channels = audio.channels
        sample_width = audio.sample_width

        return {
            "filename": file.filename,
            "duration_seconds": duration_seconds,
            "frame_rate": frame_rate,
            "channels": channels,
            "sample_width": sample_width
        }

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
