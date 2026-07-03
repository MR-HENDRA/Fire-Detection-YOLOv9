# 🔥 Fire Detection - YOLOv9

Aplikasi web deteksi kebakaran real-time menggunakan model kecerdasan buatan YOLOv9 (You Only Look Once v9).

## 📋 Deskripsi

Aplikasi ini memungkinkan pengguna untuk mengunggah gambar dan mendeteksi keberadaan api/kebakaran secara otomatis menggunakan deep learning. Aplikasi ini dibangun dengan:

- **Backend**: FastAPI (Python)
- **Model AI**: YOLOv9 (Ultralytics)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Dataset**: 5710 gambar dari Roboflow Universe

## ✨ Fitur

- 🎯 **Deteksi Real-time**: Upload gambar dan deteksi api secara instan
- 🎚️ **Adjustable Confidence**: Atur ambang kepercayaan deteksi (5% - 95%)
- 📊 **Statistik Dataset**: Lihat informasi lengkap tentang dataset training
- 🖼️ **Drag & Drop Upload**: Interface intuitif untuk upload gambar
- 📈 **Detail Deteksi**: Tabel lengkap dengan koordinat dan akurasi
- 🎨 **Modern UI**: Dark theme dengan glass morphism effect

## 🚀 Instalasi

### Prasyarat

- Python 3.8 atau lebih baru
- pip (Python package manager)

### Langkah Instalasi

1. **Clone atau download repository ini**

```bash
cd d:\A3-HXCODE
```

2. **Install dependencies**

```bash
pip install -r LOCAL/requirements.txt
```

Dependencies yang akan diinstall:
- `ultralytics` - Framework YOLOv9
- `torch` & `torchvision` - PyTorch untuk deep learning
- `fastapi` - Web framework backend
- `uvicorn` - ASGI server
- `python-multipart` - Untuk upload file
- `jinja2` - Template engine

3. **Download model YOLOv9** (otomatis saat pertama kali dijalankan)

Model `yolov9c.pt` akan otomatis diunduh saat pertama kali menjalankan aplikasi.

## 🎮 Cara Menjalankan

### Jalankan Server

```bash
python app/main.py
```

Atau menggunakan uvicorn langsung:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Akses Aplikasi

Buka browser dan akses:
```
http://localhost:8000
```

Server akan berjalan di:
- **URL**: http://localhost:8000
- **Port**: 8000
- **Docs API**: http://localhost:8000/docs (Swagger UI otomatis)

## 📁 Struktur Project

```
A3-HXCODE/
├── app/
│   ├── main.py              # FastAPI server utama
│   ├── detector.py          # Modul deteksi YOLOv9
│   ├── static/
│   │   ├── style.css        # Styling aplikasi
│   │   └── app.js           # Logic frontend
│   └── templates/
│       └── index.html       # Halaman utama
├── GOOGLE_COLAB/
│   └── colab_fire_detection.ipynb  # Notebook training di Google Colab
├── LOCAL/
│   ├── requirements.txt     # Python dependencies
│   ├── run.bat              # Script untuk menjalankan server (Windows)
│   ├── start_training.bat   # Script untuk training model (Windows)
│   ├── test_api.py          # Script testing API
│   └── train_model.py       # Script training model
├── DOCUMENTATION/
│   ├── README.md            # Dokumentasi (file ini)
│   ├── API_DOCUMENTATION.md # Dokumentasi API endpoints
│   ├── CHANGELOG.md         # Catatan perubahan
│   └── DEPLOYMENT.md        # Panduan deployment
├── .gitignore               # Git ignore file
└── README.md                # README utama repository
```

## 🔧 API Endpoints

### 1. Halaman Utama
```
GET /
```
Menampilkan antarmuka web aplikasi.

### 2. Deteksi API
```
POST /api/detect
```
**Parameters:**
- `file` (UploadFile): Gambar yang akan dideteksi
- `confidence` (float): Ambang kepercayaan (0.0 - 1.0)

**Response:**
```json
{
  "success": true,
  "data": {
    "annotated_image_base64": "...",
    "detections": [
      {
        "x1": 100.5,
        "y1": 150.2,
        "x2": 300.8,
        "y2": 400.1,
        "confidence": 92.5,
        "label": "fire"
      }
    ],
    "count": 1
  }
}
```

### 3. Statistik Dataset
```
GET /api/dataset-stats
```
**Response:**
```json
{
  "success": true,
  "data": {
    "train": {
      "images": 4000,
      "labels": 4000
    },
    "valid": {
      "images": 1000,
      "labels": 1000
    },
    "test": {
      "images": 710,
      "labels": 710
    }
  }
}
```

## 🎯 Cara Menggunakan

1. **Upload Gambar**
   - Klik area upload atau drag & drop gambar
   - Format yang didukung: JPG, PNG, WEBP
   - Maksimal ukuran: 10MB

2. **Atur Confidence Threshold**
   - Geser slider untuk mengatur sensitivitas
   - 5% - 50%: Lebih sensitif, deteksi lebih banyak (mungkin false positive)
   - 50% - 95%: Lebih akurat, hanya deteksi dengan kepercayaan tinggi

3. **Mulai Deteksi**
   - Klik tombol "Mulai Deteksi"
   - Tunggu proses AI selesai (biasanya 1-3 detik)

4. **Lihat Hasil**
   - Gambar hasil dengan bounding box merah/oranye
   - Statistik jumlah api terdeteksi
   - Tabel detail dengan koordinat dan akurasi

## 📊 Dataset Information

- **Sumber**: [Roboflow Universe - Fire Detection Dataset](https://universe.roboflow.com/ltttnt/fire-vqbia)
- **Lisensi**: CC BY 4.0
- **Total Gambar**: 5,710 gambar
- **Kelas**: 1 (Fire)
- **Resolusi**: 640 × 640 pixels
- **Split**:
  - Training: ~70%
  - Validation: ~20%
  - Testing: ~10%

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python 3.8+**
- **FastAPI**: Modern web framework untuk API
- **Ultralytics**: Library YOLOv9
- **PyTorch**: Deep learning framework
- **Pillow (PIL)**: Image processing

### Frontend
- **HTML5**: Struktur halaman
- **CSS3**: Styling dengan glass morphism
- **JavaScript (Vanilla)**: Logic tanpa framework
- **Google Fonts (Inter)**: Typography

### Model AI
- **YOLOv9c**: Compact version dari YOLOv9
- **Input Size**: 640x640
- **Classes**: 1 (Fire)
- **Architecture**: CSPNet + PAN + Detection Head

## 🔬 Cara Kerja Deteksi

1. **Upload**: User mengunggah gambar melalui web interface
2. **Preprocessing**: Gambar dikonversi ke format yang sesuai (RGB)
3. **Inference**: Model YOLOv9 memproses gambar
4. **Post-processing**: Hasil deteksi difilter berdasarkan confidence threshold
5. **Visualization**: Bounding box digambar pada gambar
6. **Response**: Hasil dikirim ke frontend dalam format JSON

## 📈 Performa

- **Inference Time**: ~0.5 - 2 detik (tergantung hardware)
- **Accuracy**: ~85-95% (tergantung confidence threshold)
- **Model Size**: ~50MB (yolov9c.pt)
- **Memory Usage**: ~2GB RAM

## 🐛 Troubleshooting

### Error: "Model tidak ditemukan"
**Solusi**: Model akan otomatis diunduh saat pertama kali. Pastikan koneksi internet aktif.

### Error: "Module not found"
**Solusi**: Install ulang dependencies:
```bash
pip install -r LOCAL/requirements.txt --upgrade
```

### Error: "Port already in use"
**Solusi**:
```bash
# Cari process yang menggunakan port 8000
netstat -ano | findstr :8000

# Hentikan process (ganti PID dengan nomor yang ditemukan)
taskkill /PID <PID> /F
```

### Deteksi Lambat
**Solusi**:
- Gunakan GPU jika tersedia (CUDA)
- Kurangi resolusi gambar input
- Gunakan model yang lebih kecil (yolov9n.pt)

### Banyak False Positive
**Solusi**: Tingkatkan confidence threshold (slider ke kanan)

### Api Tidak Terdeteksi
**Solusi**: Turunkan confidence threshold (slider ke kiri)

## 🚀 Pengembangan Lebih Lanjut

### Ideas untuk Enhancement:

1. **Video Detection**: Tambahkan deteksi pada video real-time
2. **Webcam Integration**: Deteksi dari webcam
3. **Alert System**: Kirim notifikasi saat api terdeteksi
4. **Multi-class Detection**: Tambahkan deteksi asap, dll
5. **Export Results**: Download hasil deteksi sebagai JSON/CSV
6. **Batch Processing**: Upload multiple images sekaligus
7. **Mobile Responsive**: Optimasi untuk mobile devices
8. **Dark/Light Theme**: Toggle theme
9. **History**: Simpan riwayat deteksi
10. **Custom Model**: Train model dengan dataset sendiri

### Training Custom Model:

```bash
# Install ultralytics
pip install ultralytics

# Train model (gunakan script yang sudah disediakan)
python LOCAL/train_model.py train
```

Atau gunakan Google Colab:
- Buka `GOOGLE_COLAB/colab_fire_detection.ipynb`
- Ikuti instruksi di notebook

## 📝 Lisensi

- **Code**: MIT License
- **Dataset**: CC BY 4.0
- **Model**: Ultralytics YOLOv9 (GPL-3.0)

## 👨💻 Author

**Hendra**
Proyek: A3-HXCODE
Tahun: 2026

## 🙏 Credits

- [Ultralytics YOLOv9](https://github.com/ultralytics/ultralytics)
- [Roboflow Universe](https://universe.roboflow.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- Dataset by: ltttnt

## 📧 Kontak

Jika ada pertanyaan atau masalah, silakan buat issue atau hubungi developer.

---
**🔥 Stay Safe! Detect Fire Early with AI 🔥**