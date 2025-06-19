import os
import logging
import base64
from fastapi import HTTPException

# Setup logging
logger = logging.getLogger(__name__)

async def translate_text_to_video(text: str):
    try:
        # Validasi input
        if not text or not isinstance(text, str):
            raise ValueError("Text input must be a non-empty string")
        text = text.strip()
        
        # Daftar untuk menyimpan path atau data video
        video_outputs = []
        
        # Pecah teks menjadi kata-kata berdasarkan spasi
        words = text.split()
        
        # Proses setiap kata dalam teks
        for word in words:
            # Buat path video berdasarkan kata
            video_path = f"videos/{word}.mp4"
            if not os.path.exists(video_path):
                logger.warning(f"Video untuk kata {word} tidak ditemukan di {video_path}")
                continue
            
            # Baca file video dan encode ke base64
            with open(video_path, "rb") as video_file:
                video_data = base64.b64encode(video_file.read()).decode("utf-8")
                video_outputs.append({
                    "class": word,
                    "video_data": f"data:video/mp4;base64,{video_data}"
                })
        
        if not video_outputs:
            raise ValueError("Tidak ada video yang ditemukan untuk teks yang diberikan")
        
        return {"videos": video_outputs}
    except Exception as e:
        logger.error(f"❗ Error in text to video translation: {e}")
        raise HTTPException(status_code=500, detail=str(e))