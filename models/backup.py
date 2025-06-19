import os
import logging
import base64
import io
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from tensorflow.keras.models import load_model
from PIL import Image

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fungsi untuk load labels
def load_labels(path="models/label.txt"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Label file not found at {path}")
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]

# Fungsi preprocessing gambar
def preprocess_image(image_bytes: bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((128, 128))  # Ubah ke (128, 128)
        image = np.array(image).astype("float32") / 255.0
        image = np.expand_dims(image, axis=0)  # Shape: (1, 128, 128, 3)
        return image
    except Exception as e:
        raise ValueError(f"Failed to process image: {e}")   

# Load model dan labels
model_path = "models/model_sibi.h5"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")
model = load_model(model_path)
labels = load_labels()

# Inisialisasi FastAPI dan SocketIO
app = FastAPI()
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins='*')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan origin spesifik di produksi
    allow_methods=["*"],
    allow_headers=["*"],
)
socket_app = socketio.ASGIApp(sio, app)

# Endpoint health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@sio.event
async def connect(sid, environ):
    logger.info(f"✅ Client connected: {sid}")

@sio.event
async def disconnect(sid):
    logger.info(f"❌ Client disconnected: {sid}")

@sio.event
async def frame(sid, data):
    try:
        if not isinstance(data, dict) or "image" not in data:
            raise ValueError("Invalid data format: 'image' key missing")
        image_data = data["image"]
        if not isinstance(image_data, str):
            raise ValueError("Image data must be a string")
        MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
        if len(image_data) > MAX_IMAGE_SIZE:
            raise ValueError("Image data too large")
        decoded = base64.b64decode(image_data)
        preprocessed = preprocess_image(decoded)
        prediction = model.predict(preprocessed)
        pred_class = labels[np.argmax(prediction)]
        await sio.emit("prediction", {"class": pred_class}, to=sid)
    except Exception as e:
        logger.error(f"❗ Error in frame handler: {e}")
        await sio.emit("prediction", {"class": "Error", "error": str(e)}, to=sid)

# Jalankan aplikasi menggunakan socket_app untuk mendukung WebSocket