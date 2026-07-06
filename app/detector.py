"""
Fire Detection Module using YOLOv9
===================================
Modul ini memuat model YOLOv9 dan menjalankan deteksi api pada gambar.
"""

import io
import base64
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO

# Path ke model YOLOv9 pre-trained (akan diunduh otomatis saat pertama kali dijalankan)
# Menggunakan model custom hasil training
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "RESULT_TRAINING"
    / "run_001"
    / "weights"
    / "best.pt"
)

# Singleton model agar hanya dimuat sekali
_model = None


def get_model():
    """Memuat model YOLOv9 (singleton pattern agar hemat memori)."""
    global _model
    if _model is None:
        print("[INFO] Memuat model YOLOv9... (pertama kali mungkin perlu mengunduh)")
        _model = YOLO(MODEL_PATH)
        print("[INFO] Model YOLOv9 berhasil dimuat!")
    return _model


def detect_fire(image_bytes: bytes, confidence: float = 0.25):
    """
    Menjalankan deteksi api pada gambar.

    Args:
        image_bytes: Data gambar dalam format bytes.
        confidence: Ambang batas kepercayaan deteksi (0.0 - 1.0).

    Returns:
        dict berisi:
            - annotated_image_base64: Gambar hasil deteksi dalam format base64.
            - detections: List deteksi (koordinat, confidence, label).
            - count: Jumlah api yang terdeteksi.
    """
    model = get_model()

    # Buka gambar dari bytes
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Jalankan inferensi/deteksi
    results = model.predict(source=image, conf=confidence, verbose=False)

    detections = []
    result = results[0]

    # Ambil data bounding box
    for box in result.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        label = result.names[cls]

        detections.append(
            {
                "x1": round(x1, 1),
                "y1": round(y1, 1),
                "x2": round(x2, 1),
                "y2": round(y2, 1),
                "confidence": round(conf * 100, 1),
                "label": label,
            }
        )

    # Buat gambar hasil anotasi dengan bounding box
    annotated_img = draw_detections(image, detections)

    # Konversi gambar hasil ke base64 agar bisa ditampilkan di browser
    buffer = io.BytesIO()
    annotated_img.save(buffer, format="JPEG", quality=90)
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "annotated_image_base64": img_base64,
        "detections": detections,
        "count": len(detections),
    }


def draw_detections(image: Image.Image, detections: list) -> Image.Image:
    """
    Menggambar kotak deteksi (bounding box) pada gambar.

    Args:
        image: Gambar PIL asli.
        detections: List hasil deteksi dari fungsi detect_fire.

    Returns:
        Gambar PIL dengan bounding box yang telah digambar.
    """
    draw = ImageDraw.Draw(image)

    # Warna gradien api: merah-oranye
    colors = [
        (255, 60, 30),  # Merah api
        (255, 120, 0),  # Oranye
        (255, 180, 0),  # Kuning-oranye
    ]

    for i, det in enumerate(detections):
        color = colors[i % len(colors)]
        x1, y1, x2, y2 = det["x1"], det["y1"], det["x2"], det["y2"]
        conf = det["confidence"]

        # Gambar kotak bounding box (tebal 3 pixel)
        for t in range(3):
            draw.rectangle([x1 - t, y1 - t, x2 + t, y2 + t], outline=color)

        # Label teks di atas kotak
        label_text = f"Fire {conf:.1f}%"

        # Hitung ukuran teks
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except (IOError, OSError):
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), label_text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Background untuk label
        draw.rectangle([x1, y1 - text_h - 8, x1 + text_w + 8, y1], fill=color)
        draw.text(
            (x1 + 4, y1 - text_h - 6), label_text, fill=(255, 255, 255), font=font
        )

    return image


def get_dataset_stats(dataset_path: str) -> dict:
    """
    Mengambil statistik dataset (jumlah gambar dan label per split).

    Args:
        dataset_path: Path absolut ke folder DATASET.

    Returns:
        dict berisi jumlah gambar dan label untuk train, valid, dan test.
    """
    dataset_dir = Path(dataset_path)
    stats = {}

    for split in ["train", "valid", "test"]:
        images_dir = dataset_dir / split / "images"
        labels_dir = dataset_dir / split / "labels"

        img_count = len(list(images_dir.glob("*"))) if images_dir.exists() else 0
        lbl_count = len(list(labels_dir.glob("*"))) if labels_dir.exists() else 0

        stats[split] = {"images": img_count, "labels": lbl_count}

    return stats


def get_model_info() -> dict:
    """
    Mengambil informasi model yang digunakan (metrik training).

    Returns:
        dict berisi informasi model: mAP50, mAP50-95, Precision, Recall, F1-Score, dll.
    """
    model_info_path = (
        Path(__file__).resolve().parent.parent
        / "RESULT_TRAINING"
        / "run_001"
        / "evaluation_metrics.txt"
    )

    # Default values jika file tidak ditemukan
    default_info = {
        "model_name": "YOLOv9 Custom (Fire Detection)",
        "evaluation_time": "N/A",
        "mAP50": 0.0,
        "mAP50_95": 0.0,
        "precision": 0.0,
        "recall": 0.0,
        "f1_score": 0.0,
        "training_epochs": 100,
        "image_size": 640,
        "batch_size": 16,
        "model_type": "YOLOv9c",
        "class_names": ["fire"],
    }

    if not model_info_path.exists():
        return default_info

    try:
        with open(model_info_path, "r") as f:
            lines = f.readlines()

        info = default_info.copy()
        for line in lines:
            line = line.strip()
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip().lower().replace("@", "").replace("-", "_")
                value = value.strip()

                if key in ["map50", "map_50"]:
                    info["mAP50"] = float(value)
                elif key in ["map50_95", "map_50_95"]:
                    info["mAP50_95"] = float(value)
                elif key == "precision":
                    info["precision"] = float(value)
                elif key == "recall":
                    info["recall"] = float(value)
                elif key in ["f1_score", "f1score"]:
                    info["f1_score"] = float(value)
                elif key in ["evaluation time", "evaluation date"]:
                    info["evaluation_time"] = value

        return info
    except Exception as e:
        print(f"[WARNING] Gagal membaca model info: {e}")
        return default_info
