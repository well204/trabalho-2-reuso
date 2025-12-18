import os
import uuid
import asyncio
from gtts import gTTS
from fastapi import HTTPException
from core.resilience import (
    is_circuit_open,
    register_failure,
    register_success,
    RETRY_TIMES
)

UPLOAD_DIR = "temp_files"


async def execute_tts(text: str, lang: str):
    if is_circuit_open():
        raise HTTPException(status_code=503, detail="Service unstable")

    delay = 1
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(UPLOAD_DIR, filename)

    for attempt in range(RETRY_TIMES):
        try:
            loop = asyncio.get_running_loop()

            def run_gtts():
                tts = gTTS(text=text, lang=lang)
                tts.save(filepath)

            await loop.run_in_executor(None, run_gtts)

            register_success()
            return filepath

        except Exception:
            if attempt == RETRY_TIMES - 1:
                register_failure()
                raise HTTPException(status_code=502, detail="External API failure")

            await asyncio.sleep(delay)
            delay *= 2