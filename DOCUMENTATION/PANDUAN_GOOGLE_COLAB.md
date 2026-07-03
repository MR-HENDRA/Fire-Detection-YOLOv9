# 🚀 Panduan Lengkap Training YOLOv9 di Google Colab (GRATIS)

## Persiapan

### 1. Upload Dataset ke Google Drive
**Cara 1: Manual Upload**
1. Buka [Google Drive](https://drive.google.com)
2. Buat folder baru: `YOLOv9_Fire_Detection`
3. Upload folder `FIRE DETECTION USING YOLOV9` ke folder tersebut
4. Pastikan struktur:
   ```
   Google Drive/
   └── YOLOv9_Fire_Detection/
       └── FIRE DETECTION USING YOLOV9/
           └── DATASET/
               ├── train/
               │   ├── images/
               │   └── labels/
               ├── valid/
               │   ├── images/
               │   └── labels/
               ├── test/
               │   ├── images/
               │   └── labels/
               └── data.yaml
   ```

**Cara 2: Mount Google Drive di Colab**
- Lebih mudah, lihat langkah 3 di bawah

---

### 2. Buka Google Colab
1. Buka [Google Colab](https://colab.research.google.com)
2. Klik **New Notebook** (File > New Notebook)
3. Ganti nama notebook: `Fire_Detection_YOLOv9_Training`

---

## 📝 Script Lengkap untuk Colab

```python
# =============================================
# STEP 1: Install Ultralytics YOLOv9
# =============================================
!pip install ultralytics
print("✅ Ultralytics YOLOv9 terinstall")

# =============================================
# STEP 2: Mount Google Drive
# =============================================
from google.colab import drive
drive.mount('/content/drive')

# =============================================
# STEP 3: Set Path Dataset
# =============================================
# Ganti path sesuai lokasi dataset Anda di Google Drive
DATASET_PATH = "/content/drive/MyDrive/YOLOv9_Fire_Detection/FIRE DETECTION USING YOLOV9/DATASET/data.yaml"

# Cek apakah dataset ada
import os
if not os.path.exists(DATASET_PATH):
    print(f"❌ Dataset tidak ditemukan di: {DATASET_PATH}")
    print("Pastikan Anda sudah upload dataset ke Google Drive!")
else:
    print(f"✅ Dataset ditemukan di: {DATASET_PATH}")

# =============================================
# STEP 4: Training Model
# =============================================
from ultralytics import YOLO
import torch

# Cek GPU
device = "0" if torch.cuda.is_available() else "cpu"
print(f"🔥 Menggunakan device: {'GPU' if device == '0' else 'CPU'}")

# Load model
print("📦 Loading pretrained model yolov9c.pt...")
model = YOLO("yolov9c.pt")

# Start training
print("🚀 Starting training...")
results = model.train(
    data=DATASET_PATH,
    epochs=50,           # Jumlah epoch
    imgsz=640,           # Ukuran gambar (bisa 640 karena pakai GPU)
    batch=16,            # Batch size (GPU Colab kuat)
    name="fire_detection_yolov9_colab",
    patience=20,         # Early stopping
    device=device,       # Pakai GPU
    workers=2,          # Dataloader workers
    verbose=True,
    plots=True,
)

print("✅ Training selesai!")

# =============================================
# STEP 5: Validation
# =============================================
print("🔍 Validating model...")
model_path = "/content/runs/detect/fire_detection_yolov9_colab/weights/best.pt"
model = YOLO(model_path)

results = model.val(
    data=DATASET_PATH,
    imgsz=640,
    batch=16,
    device=device,
)

print(f"✅ Validation selesai!")
print(f"mAP50: {results.box.map50:.4f}")
print(f"mAP50-95: {results.box.map:.4f}")

# =============================================
# STEP 6: Export Model (Optional)
# =============================================
# Export ke ONNX
print("📤 Exporting to ONNX...")
model.export(format="onnx")
print("✅ Model ONNX tersimpan di: /content/runs/detect/fire_detection_yolov9_colab/weights/best.onnx")

# Export ke TFLite
print("📤 Exporting to TFLite...")
model.export(format="tflite")
print("✅ Model TFLite tersimpan di: /content/runs/detect/fire_detection_yolov9_colab/weights/best.tflite")

# =============================================
# STEP 7: Download Hasil
# =============================================
from google.colab import files

# Download model best.pt
files.download("/content/runs/detect/fire_detection_yolov9_colab/weights/best.pt")
print("✅ best.pt sudah didownload")

# Download model ONNX
files.download("/content/runs/detect/fire_detection_yolov9_colab/weights/best.onnx")
print("✅ best.onnx sudah didownload")