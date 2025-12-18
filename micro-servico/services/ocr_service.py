import asyncio
import pytesseract as tess
from PIL import Image
from fastapi import HTTPException
from core.resilience import bulkhead_semaphore


async def execute_ocr(image_path: str, lang: str):
    if not bulkhead_semaphore.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="Server busy")

    try:
        loop = asyncio.get_running_loop()
        tess_lang = 'por' if lang == 'pt' else 'eng'

        def run_tesseract():
            img = Image.open(image_path)
            return tess.image_to_string(img, lang=tess_lang)

        text = await loop.run_in_executor(None, run_tesseract)
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        bulkhead_semaphore.release()