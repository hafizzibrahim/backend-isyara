# Backend Isyara - Penerjemah Bahasa Isyarat Indonesia (SIBI)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.78%2B-green.svg)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)

Backend ini menyediakan layanan untuk menerjemahkan Bahasa Isyarat Indonesia (SIBI) secara real-time dari gambar (streaming) ke teks, dan sebaliknya dari teks ke video peraga isyarat.

## ✨ Fitur Utama

1.  **Penerjemah Isyarat ke Teks (Real-time)**
    -   Menerima frame gambar melalui koneksi WebSocket (Socket.IO).
    -   Memproses gambar menggunakan model Deep Learning untuk mengenali gestur isyarat.
    -   Mengirimkan hasil prediksi teks kembali ke klien.

2.  **Penerjemah Teks ke Video Isyarat**
    -   Menyediakan endpoint API untuk menerima input berupa kalimat.
    -   Mengonversi kalimat menjadi serangkaian video peraga isyarat kata per kata.
    -   Mengembalikan daftar URL video yang sesuai dengan teks input.

## 🛠️ Teknologi yang Digunakan

-   **Web Framework**: FastAPI
-   **Real-time Communication**: Python Socket.IO
-   **Machine Learning**: TensorFlow & Keras
-   **Image Processing**: OpenCV & Pillow
-   **Server**: Uvicorn

## 🚀 Instalasi & Persiapan

Pastikan Anda memiliki Python 3.9 atau versi lebih baru.

1.  **Clone Repositori**
    ```bash
    git clone https://github.com/username/backend-isyara.git
    cd backend-isyara
    ```

2.  **Buat dan Aktifkan Virtual Environment** (Opsional tapi direkomendasikan)
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependensi**
    Pastikan semua library yang dibutuhkan ter-install dengan menjalankan perintah:
    ```bash
    pip install -r requirement.txt
    ```

4.  **Download Model**
    Pastikan file model `.h5` sudah tersedia di dalam direktori `models/`.

## 🏃‍♂️ Menjalankan Aplikasi

Untuk menjalankan server, gunakan perintah berikut dari direktori utama proyek:

```bash
python main.py
```

Server akan berjalan di `http://0.0.0.0:8000`.

Anda dapat memeriksa apakah server berjalan dengan baik dengan mengakses endpoint health check: `http://localhost:8000/health`.

## 🔌 Detail API

### WebSocket (Socket.IO)

-   **Koneksi**: Klien dapat terhubung ke server melalui Socket.IO.
-   **Event `frame`**: Klien mengirimkan frame gambar (dalam format yang sesuai, misal base64) ke event ini untuk diproses.
    -   **Payload**: `data` (string base64 atau bytes dari gambar)
-   **Event `prediction`** (Contoh): Server akan mengirimkan hasil prediksi melalui event ini.
    -   **Payload**: `{"text": "hasil_prediksi"}`

### HTTP Endpoints

-   **`GET /health`**
    -   **Deskripsi**: Untuk memeriksa status server.
    -   **Response**: `{"status": "healthy"}`

-   **`POST /translate`**
    -   **Deskripsi**: Menerjemahkan sebuah kalimat menjadi video isyarat.
    -   **Request Body**:
        ```json
        {
          "text": "contoh kalimat"
        }
        ```
    -   **Response Sukses**:
        ```json
        {
          "videos": ["/videos/contoh.mp4", "/videos/kalimat.mp4"]
        }
        ```

## 📂 Struktur Proyek

```
.
├──  D:/Project/backend-isyara
│   ├── main.py             # Entry point aplikasi FastAPI & Socket.IO
│   ├── image_prediction.py # Logika untuk prediksi gambar isyarat
│   ├── text_to_video.py    # Logika untuk terjemahan teks ke video
│   ├── requirement.txt     # Daftar dependensi Python
│   ├── models/             # Direktori berisi model-model machine learning (.h5)
│   ├── videos/             # Direktori berisi video peraga isyarat
│   └── photo/              # Direktori untuk menyimpan gambar yang diterima
└── ...
```
