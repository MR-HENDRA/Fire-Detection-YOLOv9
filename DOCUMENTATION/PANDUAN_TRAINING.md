# 🚀 Panduan Training - Fire Detection YOLOv9

## ✅ Persiapan Selesai!

Semua file sudah siap untuk training:
- ✅ Dataset: 1000+ gambar api
- ✅ Konfigurasi: Sudah disesuaikan untuk CPU
- ✅ Script training: Siap dijalankan
- ✅ Batch file: `start_training.bat` sudah dibuat

---

## 📋 Langkah-langkah Training

### 1️⃣ Stop Web App (Jika Running)

**Di terminal yang menjalankan web app:**
```
Tekan: Ctrl + C
```

Pastikan terminal tidak lagi menjalankan `python app/main.py`

---

### 2️⃣ Mulai Training

**Pilihan A: Double-click file (MUDAH)**
```
Double-click file: start_training.bat
```

**Pilihan B: Manual via terminal**
```bash
python train_model.py train
```

---

### 3️⃣ Tunggu Training Selesai

Anda akan melihat output seperti ini:

```
============================================================
🔥 Fire Detection - YOLOv9 Training
============================================================
[INFO] Dataset: FIRE DETECTION USING YOLOV9/DATASET/data.yaml
[INFO] Model: yolov9c.pt
[INFO] Epochs: 50
[INFO] Image Size: 640
[INFO] Batch Size: 8
============================================================
[INFO] Loading pretrained model...
Downloading https://github.com/ultralytics/assets/releases/download/v8.4.0/yolov9c.pt...
[INFO] Starting training...
============================================================

Epoch 1/50: 100%|██████████| 125/125 [03:45<00:00,  1.80s/it]
      Class     Images  Instances      Box(P          R      mAP50  mAP50-95)
        all        200        300      0.456      0.567      0.512     0.289

Epoch 2/50: 100%|██████████| 125/125 [03:42<00:00,  1.78s/it]
      Class     Images  Instances      Box(P          R      mAP50  mAP50-95)
        all        200        300      0.523      0.645      0.598     0.356

... (akan berlanjut sampai epoch 50)
```

**Apa artinya:**
- **Epoch X/50**: Progress training (0-50)
- **Box(P)**: Precision (ketelitian)
- **R**: Recall (kemampuan mendeteksi)
- **mAP50**: Mean Average Precision (akurasi keseluruhan)
- Semakin tinggi angkanya, semakin bagus!

---

### 4️⃣ Estimasi Waktu

| Tipe CPU | Estimasi Waktu |
|----------|----------------|
| Intel i3 / Ryzen 3 | 3-4 jam |
| Intel i5 / Ryzen 5 | 2-3 jam |
| Intel i7 / Ryzen 7 | 1.5-2 jam |
| Dengan GPU CUDA | 30-60 menit |

**Tips selama training:**
- ✅ Biarkan komputer menyala
- ✅ Jangan tutup terminal
- ✅ Boleh browsing/kerja lain (training di background)
- ✅ Jangan restart komputer
- ⚠️ Koneksi internet perlu hanya di awal (download model)

---

### 5️⃣ Training Selesai!

Ketika selesai, Anda akan melihat:

```
============================================================
✅ Training selesai!
[INFO] Model tersimpan di: runs/detect/fire_detection_yolov9/
[INFO] Best model: runs/detect/fire_detection_yolov9/weights/best.pt
============================================================
```

**File hasil training:**
```
runs/
└── detect/
    └── fire_detection_yolov9/
        ├── weights/
        │   ├── best.pt      ← Model terbaik (gunakan ini!)
        │   └── last.pt      ← Model terakhir
        ├── results.png      ← Grafik hasil training
        ├── confusion_matrix.png
        └── ... (file lainnya)
```

---

### 6️⃣ Update Kode untuk Gunakan Model Baru

**Edit file: `app/detector.py`**

Cari baris ini:
```python
MODEL_PATH = "yolov9c.pt"
```

Ganti menjadi:
```python
MODEL_PATH = "runs/detect/fire_detection_yolov9/weights/best.pt"
```

**Atau jalankan command ini:**
```python
# Saya akan bantu update otomatis setelah training selesai
```

---

### 7️⃣ Test Model Baru

```bash
# Jalankan web app
python app/main.py

# Buka browser
http://localhost:5000

# Upload gambar api
# Hasilnya harus: fire 90%+ ✅
```

---

## 🆘 Troubleshooting

### ❌ "Out of Memory Error"

**Solusi:** Kurangi batch size di `train_model.py`:
```python
CONFIG = {
    "batch": 4,  # Ubah dari 8 ke 4
    # ... sisanya sama
}
```

### ❌ "CUDA not available"

Ini NORMAL jika tidak punya GPU NVIDIA. Training akan menggunakan CPU (lebih lambat tapi tetap berhasil).

### ❌ Training terlalu lama

**Opsi 1:** Kurangi epochs di `train_model.py`:
```python
CONFIG = {
    "epochs": 30,  # Ubah dari 50 ke 30
    # ... sisanya sama
}
```

**Opsi 2:** Biarkan training berjalan overnight (semalam)

### ❌ "Dataset not found"

Pastikan struktur folder benar:
```
FIRE DETECTION USING YOLOV9/
└── DATASET/
    ├── data.yaml
    ├── train/images/
    ├── train/labels/
    ├── valid/images/
    └── valid/labels/
```

---

## 📊 Memahami Hasil Training

### Grafik `results.png`

Akan menampilkan:
- **Box Loss**: Harus turun (semakin rendah semakin bagus)
- **mAP50**: Harus naik (target: >0.8 atau 80%)
- **Precision**: Harus naik (target: >0.85 atau 85%)
- **Recall**: Harus naik (target: >0.80 atau 80%)

### Model yang Bagus:
```
mAP50: 0.85-0.95 (85-95%)
Precision: 0.85-0.95
Recall: 0.80-0.90
```

### Model yang Cukup Bagus:
```
mAP50: 0.70-0.85 (70-85%)
Precision: 0.75-0.85
Recall: 0.70-0.80
```

---

## ✅ Checklist Training

```
[ ] 1. Stop web app (Ctrl+C)
[ ] 2. Double-click start_training.bat
[ ] 3. Tunggu 2-4 jam
[ ] 4. Training selesai
[ ] 5. Update MODEL_PATH di app/detector.py
[ ] 6. Test dengan python app/main.py
[ ] 7. Upload gambar api dan lihat hasilnya!
```

---

## 🎉 Setelah Training

Model Anda akan bisa mendeteksi api dengan akurasi tinggi:

**Sebelum:**
```
❌ person (75%)
❌ oven (37%)
❌ microwave (36%)
```

**Setelah:**
```
✅ fire (92%)
✅ fire (88%)
✅ fire (85%)
```

---

## 💡 Tips Pro

1. **Simpan model backup**
   ```bash
   copy "runs\detect\fire_detection_yolov9\weights\best.pt" "best_fire_model_backup.pt"
   ```

2. **Lihat hasil training**
   ```bash
   start runs\detect\fire_detection_yolov9\results.png
   ```

3. **Validasi model**
   ```bash
   python train_model.py validate
   ```

4. **Export ke format lain**
   ```bash
   python train_model.py export onnx
   ```

---

## ❓ Pertanyaan?

Jika ada masalah atau pertanyaan selama training, jangan ragu untuk bertanya! 😊

**Siap mulai training?** 
- Double-click: `start_training.bat`
- Atau ketik: `python train_model.py train`

Good luck! 🔥🚀
