import os
from fastapi import FastAPI
from routers import api

UPLOAD_DIR = "temp_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

app.include_router(api.router)