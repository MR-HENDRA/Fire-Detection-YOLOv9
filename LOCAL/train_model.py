"""
Fire Detection - YOLOv9 Training Script
========================================
Script untuk melatih model YOLOv9 dengan dataset custom.
"""

from ultralytics import YOLO
import os
from pathlib import Path

# Konfigurasi Training
CONFIG = {
    "data": "LOCAL/DATASET/data.yaml",
    "model": "yolov9c.pt",  # Pretrained model
    "epochs": 50,  # Dikurangi dari 100 untuk training lebih cepat
    "imgsz": 640,
    "batch": 4,  # Dikurangi dari 8 untuk menghindari out of memory pada laptop
    "name": "fire_detection_yolov9",
    "patience": 20,  # Early stopping
    "device": "cpu",  # Gunakan CPU (ubah ke 0 jika punya GPU CUDA)
    "workers": 0,  # Nonaktifkan workers untuk menghindari memory leak
}

def train():
    """Fungsi utama untuk training model."""
    print("=" * 60)
    print("🔥 Fire Detection - YOLOv9 Training")
    print("=" * 60)
    
    # Cek apakah dataset ada
    dataset_path = Path(CONFIG["data"])
    if not dataset_path.exists():
        print(f"[ERROR] Dataset tidak ditemukan: {CONFIG['data']}")
        print("Pastikan folder DATASET sudah ada dan berisi data training.")
        return
    
    print(f"[INFO] Dataset: {CONFIG['data']}")
    print(f"[INFO] Model: {CONFIG['model']}")
    print(f"[INFO] Epochs: {CONFIG['epochs']}")
    print(f"[INFO] Image Size: {CONFIG['imgsz']}")
    print(f"[INFO] Batch Size: {CONFIG['batch']}")
    print("=" * 60)
    
    # Load pretrained model
    print("[INFO] Loading pretrained model...")
    model = YOLO(CONFIG["model"])
    
    # Start training
    print("[INFO] Starting training...")
    print("[TIP] Training akan memakan waktu lama (bisa berjam-jam)")
    print("[TIP] Tekan Ctrl+C untuk menghentikan training")
    print("=" * 60)
    
    try:
        results = model.train(
            data=CONFIG["data"],
            epochs=CONFIG["epochs"],
            imgsz=CONFIG["imgsz"],
            batch=CONFIG["batch"],
            name=CONFIG["name"],
            patience=CONFIG["patience"],
            device=CONFIG["device"],
            workers=CONFIG["workers"],
            verbose=True,
            plots=True,
        )
        
        print("=" * 60)
        print("✅ Training selesai!")
        print(f"[INFO] Model tersimpan di: runs/detect/{CONFIG['name']}/")
        print(f"[INFO] Best model: runs/detect/{CONFIG['name']}/weights/best.pt")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n[WARNING] Training dihentikan oleh user.")
    except Exception as e:
        print(f"\n[ERROR] Training gagal: {e}")

def validate():
    """Validasi model yang sudah di-train."""
    print("=" * 60)
    print("🔥 Fire Detection - YOLOv9 Validation")
    print("=" * 60)
    
    model_path = f"runs/detect/{CONFIG['name']}/weights/best.pt"
    
    if not Path(model_path).exists():
        print(f"[ERROR] Model tidak ditemukan: {model_path}")
        print("Jalankan training terlebih dahulu dengan: python train_model.py")
        return
    
    print(f"[INFO] Loading model: {model_path}")
    model = YOLO(model_path)
    
    print("[INFO] Validating model...")
    results = model.val(
        data=CONFIG["data"],
        imgsz=CONFIG["imgsz"],
        batch=CONFIG["batch"],
    )
    
    print("=" * 60)
    print("✅ Validation selesai!")
    print(f"[INFO] mAP50: {results.box.map50:.4f}")
    print(f"[INFO] mAP50-95: {results.box.map:.4f}")
    print("=" * 60)

def export_model(format="onnx"):
    """Export model ke format lain (ONNX, TFLite, dll)."""
    print("=" * 60)
    print(f"🔥 Fire Detection - Export Model ke {format.upper()}")
    print("=" * 60)
    
    model_path = f"runs/detect/{CONFIG['name']}/weights/best.pt"
    
    if not Path(model_path).exists():
        print(f"[ERROR] Model tidak ditemukan: {model_path}")
        return
    
    print(f"[INFO] Loading model: {model_path}")
    model = YOLO(model_path)
    
    print(f"[INFO] Exporting to {format}...")
    model.export(format=format)
    
    print("=" * 60)
    print(f"✅ Model berhasil di-export ke format {format.upper()}!")
    print("=" * 60)

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "train":
            train()
        elif command == "validate" or command == "val":
            validate()
        elif command == "export":
            format_type = sys.argv[2] if len(sys.argv) > 2 else "onnx"
            export_model(format_type)
        else:
            print("Usage:")
            print("  python train_model.py train        - Train model")
            print("  python train_model.py validate     - Validate trained model")
            print("  python train_model.py export onnx  - Export model to ONNX")
    else:
        # Default: training
        train()
