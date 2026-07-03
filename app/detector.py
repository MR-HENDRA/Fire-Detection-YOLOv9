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
MODEL_PATH = "../LOCAL/yolov9c.pt"

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

        detections.append({
            "x1": round(x1, 1),
            "y1": round(y1, 1),
            "x2": round(x2, 1),
            "y2": round(y2, 1),
            "confidence": round(conf * 100, 1),
            "label": label
        })

    # Buat gambar hasil anotasi dengan bounding box
    annotated_img = draw_detections(image, detections)

    # Konversi gambar hasil ke base64 agar bisa ditampilkan di browser
    buffer = io.BytesIO()
    annotated_img.save(buffer, format="JPEG", quality=90)
    img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return {
        "annotated_image_base64": img_base64,
        "detections": detections,
        "count": len(detections)
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
        (255, 60, 30),   # Merah api
        (255, 120, 0),   # Oranye
        (255, 180, 0),   # Kuning-oranye
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
        draw.rectangle(
            [x1, y1 - text_h - 8, x1 + text_w + 8, y1],
            fill=color
        )
        draw.text((x1 + 4, y1 - text_h - 6), label_text, fill=(255, 255, 255), font=font)

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

        stats[split] = {
            "images": img_count,
            "labels": lbl_count
        }

    return stats
