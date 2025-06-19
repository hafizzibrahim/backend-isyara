import base64
import io
import numpy as np
import logging
from PIL import Image
from tensorflow.keras.models import load_model
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

# Load model dan label hanya sekali (global)
MODEL_PATH = "models/sibi_modifikasi.h5"
LABEL_PATH = "models/label.txt"

model = load_model(MODEL_PATH)
labels = [line.strip() for line in open(LABEL_PATH)]
prediction_history = defaultdict(lambda: deque(maxlen=5))

def preprocess_image(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    w, h = image.size
    target_size = 144
    scale = target_size / max(w, h)
    new_w, new_h = int(w * scale), int(h * scale)
    image = image.resize((new_w, new_h))

    padded = Image.new("RGB", (target_size, target_size), color=(0, 0, 0))
    left = (target_size - new_w) // 2
    top = (target_size - new_h) // 2
    padded.paste(image, (left, top))

    arr = np.array(padded).astype("float32") / 255.0
    return np.expand_dims(arr, axis=0)

async def handle_frame(sid, data, sio):
    try:
        if "image" not in data:
            raise ValueError("Data tidak memiliki key 'image'")

        image_data = base64.b64decode(data["image"])

        with open("photo/last_received.jpg", "wb") as f:
            f.write(image_data)

        preprocessed = preprocess_image(image_data)

        prediction = model.predict(preprocessed)
        pred_index = np.argmax(prediction)
        pred_class = labels[pred_index]
        pred_prob = float(prediction[0][pred_index])

        prediction_history[sid].append(pred_class)
        counts = {cls: prediction_history[sid].count(cls) for cls in set(prediction_history[sid])}
        most_common = max(counts, key=counts.get)

        if counts[most_common] >= 3 and pred_prob >= 0.5:
            await sio.emit("prediction", {"class": most_common, "probability": pred_prob}, to=sid)
            logger.info(f"🎯 Stabil prediksi: {most_common} | Prob: {pred_prob:.4f}")
        else:
            await sio.emit("prediction", {"class": "...", "probability": pred_prob}, to=sid)

    except Exception as e:
        logger.error(f"❗ Error saat handle_frame: {e}", exc_info=True)
        await sio.emit("prediction", {"class": "Error", "error": str(e)}, to=sid)
