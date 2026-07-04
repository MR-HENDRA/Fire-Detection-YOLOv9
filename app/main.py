"""
Fire Detection Web Server
==========================
Server FastAPI untuk menyajikan antarmuka web deteksi kebakaran
dan memproses gambar yang diunggah pengguna.
"""

import os
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from detector import detect_fire, get_dataset_stats, get_model_info

# Konfigurasi path
BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR.parent / "LOCAL" / "DATASET"

# Inisialisasi FastAPI
app = FastAPI(
    title="🔥 Fire Detection - YOLOv9",
    description="Aplikasi deteksi kebakaran menggunakan YOLOv9",
    version="1.0.0"
)

# Mount folder static (CSS, JS)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Template HTML
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Halaman utama aplikasi."""
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/api/detect")
async def api_detect(
    file: UploadFile = File(...),
    confidence: float = Form(0.25)
):
    """
    API endpoint untuk mendeteksi api pada gambar yang diunggah.

    Args:
        file: File gambar yang diunggah.
        confidence: Ambang batas kepercayaan deteksi (0-1).

    Returns:
        JSON berisi gambar hasil anotasi (base64), daftar deteksi, dan jumlah api.
    """
    try:
        # Baca file gambar
        image_bytes = await file.read()

        # Jalankan deteksi
        result = detect_fire(image_bytes, confidence=confidence)

        return JSONResponse(content={
            "success": True,
            "data": result
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@app.get("/api/dataset-stats")
async def api_dataset_stats():
    """
    API endpoint untuk mengambil statistik dataset.

    Returns:
        JSON berisi jumlah gambar dan label per split (train/valid/test).
    """
    try:
        stats = get_dataset_stats(str(DATASET_DIR))
        # Jika dataset tidak ditemukan, gunakan data default
        if stats.get("train", {}).get("images", 0) == 0:
            stats = {
                "train": {"images": 4808, "labels": 4808},
                "valid": {"images": 601, "labels": 601},
                "test": {"images": 301, "labels": 301}
            }
        return JSONResponse(content={
            "success": True,
            "data": stats
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@app.get("/api/model-info")
async def api_model_info():
    """
    API endpoint untuk mengambil informasi model yang digunakan.

    Returns:
        JSON berisi informasi model: mAP50, mAP50-95, Precision, Recall, F1-Score, dll.
    """
    try:
        model_info = get_model_info()
        return JSONResponse(content={
            "success": True,
            "data": model_info
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("🔥 Fire Detection App - YOLOv9")
    print("=" * 60)
    print("Buka browser dan akses: http://localhost:8000")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
