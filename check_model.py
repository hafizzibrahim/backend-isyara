import tensorflow as tf
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_model_summary(model_path="models/sibi_modifikasi.h5"):
    try:
        # Periksa apakah file model ada
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        # Muat model
        model = tf.keras.models.load_model(model_path)
        
        # Cetak ringkasan model
        logger.info("Model Summary:")
        model.summary()
        
        # Opsional: Cetak input shape yang diharapkan
        logger.info(f"Model input shape: {model.input_shape}")
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")

if __name__ == "__main__":
    check_model_summary()