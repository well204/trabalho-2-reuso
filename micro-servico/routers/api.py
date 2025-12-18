import shutil
import os
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from services.ocr_service import execute_ocr
from services.tts_service import execute_tts
from core.resilience import is_circuit_open, circuit_failures, bulkhead_semaphore

router = APIRouter()
UPLOAD_DIR = "temp_files"


@router.post("/image-to-text")
async def image_to_text(file: UploadFile = File(...), lang: str = Form("pt")):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = await execute_ocr(file_location, lang)
    finally:
        if os.path.exists(file_location):
            os.remove(file_location)

    if not text.strip():
        return {"status": "warning", "text": ""}

    return {"status": "success", "text": text.strip()}


@router.post("/text-to-speech")
async def text_to_speech(text: str = Form(...), lang: str = Form("pt")):
    if not text:
        raise HTTPException(400, "Empty text")

    audio_path = await execute_tts(text, lang)
    return FileResponse(audio_path, media_type="audio/mpeg", filename="audio.mp3")


@router.post("/image-to-speech-full")
async def image_to_speech_full(file: UploadFile = File(...), lang: str = Form("pt")):
    file_location = os.path.join(UPLOAD_DIR, f"temp_{uuid.uuid4()}.png")
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = await execute_ocr(file_location, lang)

        if not extracted_text.strip():
            raise HTTPException(400, "No text detected")

        audio_path = await execute_tts(extracted_text, lang)
        return FileResponse(audio_path, media_type="audio/mpeg", filename="speech.mp3")

    finally:
        if os.path.exists(file_location):
            os.remove(file_location)


@router.get("/health")
async def health_check():
    return {
        "status": "online",
        "resilience": {
            "circuit_open": is_circuit_open(),
            "failures": circuit_failures,
            "bulkhead_free": bulkhead_semaphore._value
        }
    }