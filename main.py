import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from image_prediction import handle_frame
from text_to_video import translate_text_to_video
from pydantic import BaseModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi FastAPI dan SocketIO
app = FastAPI()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan origin spesifik di produksi
    allow_methods=["*"],
    allow_headers=["*"],
)
socket_app = socketio.ASGIApp(sio, app)

# Model untuk validasi input teks
class TextInput(BaseModel):
    text: str

# Endpoint health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Endpoint untuk menerjemahkan teks ke video
@app.post("/translate")
async def translate(input: TextInput):
    return await translate_text_to_video(input.text)

# Event SocketIO
@sio.event
async def connect(sid, environ):
    logger.info(f"✅ Client connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"❌ Client disconnected: {sid}")

@sio.event
async def frame(sid, data):
    await handle_frame(sid, data, sio)

# Jalankan aplikasi menggunakan socket_app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)