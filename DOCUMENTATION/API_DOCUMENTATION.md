# 📚 API Documentation - Fire Detection YOLOv9

Dokumentasi lengkap untuk API endpoints aplikasi Fire Detection.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. Home Page

**Endpoint**: `GET /`

**Description**: Menampilkan halaman utama aplikasi web.

**Response**: HTML Page

**Example**:
```bash
curl http://localhost:8000
```

---

### 2. Fire Detection API

**Endpoint**: `POST /api/detect`

**Description**: Mendeteksi keberadaan api dalam gambar yang diunggah.

**Request**:
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file` (required): File gambar yang akan dideteksi
  - `confidence` (optional): Ambang kepercayaan deteksi (0.0 - 1.0), default: 0.25

**Response**:
```json
{
  "success": true,
  "data": {
    "annotated_image_base64": "iVBORw0KGgoAAAANSUhEUgA...",
    "detections": [
      {
        "x1": 120.5,
        "y1": 180.2,
        "x2": 320.8,
        "y2": 450.1,
        "confidence": 92.5,
        "label": "fire"
      },
      {
        "x1": 450.0,
        "y1": 200.0,
        "x2": 600.0,
        "y2": 400.0,
        "confidence": 87.3,
        "label": "fire"
      }
    ],
    "count": 2
  }
}
```

**Error Response**:
```json
{
  "success": false,
  "error": "Error message here"
}
```

**Example - cURL**:
```bash
curl -X POST http://localhost:8000/api/detect \
  -F "file=@path/to/image.jpg" \
  -F "confidence=0.5"
```

**Example - Python**:
```python
import requests

url = "http://localhost:8000/api/detect"
files = {"file": open("image.jpg", "rb")}
data = {"confidence": 0.5}

response = requests.post(url, files=files, data=data)
result = response.json()

if result["success"]:
    print(f"Detected {result['data']['count']} fire(s)")
    for i, detection in enumerate(result['data']['detections']):
        print(f"Fire {i+1}: {detection['confidence']}% confidence")
else:
    print(f"Error: {result['error']}")
```

**Example - JavaScript (Fetch)**:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('confidence', 0.5);

fetch('http://localhost:8000/api/detect', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log(`Detected ${data.data.count} fire(s)`);
        data.data.detections.forEach((det, i) => {
            console.log(`Fire ${i+1}: ${det.confidence}% confidence`);
        });
    } else {
        console.error('Error:', data.error);
    }
});
```

---

### 3. Dataset Statistics API

**Endpoint**: `GET /api/dataset-stats`

**Description**: Mengambil statistik dataset (jumlah gambar dan label per split).

**Response**:
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

**Error Response**:
```json
{
  "success": false,
  "error": "Error message here"
}
```

**Example - cURL**:
```bash
curl http://localhost:8000/api/dataset-stats
```

**Example - Python**:
```python
import requests

response = requests.get("http://localhost:8000/api/dataset-stats")
result = response.json()

if result["success"]:
    stats = result["data"]
    print(f"Training: {stats['train']['images']} images")
    print(f"Validation: {stats['valid']['images']} images")
    print(f"Testing: {stats['test']['images']} images")
```

---

## Response Fields

### Detection Object

| Field | Type | Description |
|-------|------|-------------|
| `x1` | float | Koordinat X kiri atas bounding box |
| `y1` | float | Koordinat Y kiri atas bounding box |
| `x2` | float | Koordinat X kanan bawah bounding box |
| `y2` | float | Koordinat Y kanan bawah bounding box |
| `confidence` | float | Tingkat kepercayaan deteksi (0-100%) |
| `label` | string | Label kelas yang terdeteksi (selalu "fire") |

### Dataset Stats Object

| Field | Type | Description |
|-------|------|-------------|
| `images` | integer | Jumlah gambar dalam split |
| `labels` | integer | Jumlah file label dalam split |

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Success - Request berhasil |
| 400 | Bad Request - Parameter tidak valid |
| 500 | Internal Server Error - Terjadi kesalahan server |

---

## Rate Limiting

Saat ini tidak ada rate limiting. Untuk production, disarankan menambahkan rate limiting untuk mencegah abuse.

---

## CORS Policy

Default CORS sudah diaktifkan untuk semua origin. Untuk production, sesuaikan CORS policy sesuai kebutuhan.

---

## Image Requirements

### Supported Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- BMP (.bmp)
- TIFF (.tiff)

### Size Limits
- Maximum file size: 10 MB
- Recommended resolution: 640x640 pixels
- Minimum resolution: 320x320 pixels

### Best Practices
1. Gunakan gambar dengan pencahayaan yang baik
2. Pastikan objek api terlihat jelas
3. Hindari gambar yang terlalu blur atau gelap
4. Untuk hasil optimal, gunakan confidence threshold 0.25 - 0.5

---

## Error Handling

### Common Errors

**1. File too large**
```json
{
  "success": false,
  "error": "File size exceeds 10MB limit"
}
```

**2. Invalid file format**
```json
{
  "success": false,
  "error": "Invalid image format. Supported: JPG, PNG, WEBP"
}
```

**3. Model not loaded**
```json
{
  "success": false,
  "error": "Model YOLOv9 failed to load"
}
```

**4. Dataset not found**
```json
{
  "success": false,
  "error": "Dataset directory not found"
}
```

---

## Swagger UI (Interactive API Docs)

FastAPI secara otomatis menyediakan dokumentasi interaktif:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Dokumentasi ini memungkinkan Anda untuk:
- Melihat semua endpoints
- Mencoba API langsung dari browser
- Melihat request/response schema
- Generate code samples

---

## Integration Examples

### Example 1: Batch Processing

```python
import requests
from pathlib import Path

def batch_detect(image_folder, confidence=0.25):
    """Detect fire in multiple images."""
    url = "http://localhost:8000/api/detect"
    results = []
    
    for img_path in Path(image_folder).glob("*.jpg"):
        with open(img_path, "rb") as f:
            files = {"file": f}
            data = {"confidence": confidence}
            response = requests.post(url, files=files, data=data)
            
            result = response.json()
            if result["success"]:
                results.append({
                    "image": img_path.name,
                    "fire_count": result["data"]["count"],
                    "detections": result["data"]["detections"]
                })
    
    return results

# Usage
results = batch_detect("./images", confidence=0.4)
for r in results:
    print(f"{r['image']}: {r['fire_count']} fire(s) detected")
```

### Example 2: Real-time Alert System

```python
import requests
import time
from pathlib import Path

def monitor_folder(folder, interval=5):
    """Monitor folder for new images and detect fire."""
    url = "http://localhost:8000/api/detect"
    processed = set()
    
    while True:
        for img_path in Path(folder).glob("*.jpg"):
            if img_path not in processed:
                with open(img_path, "rb") as f:
                    response = requests.post(url, files={"file": f})
                    result = response.json()
                    
                    if result["success"] and result["data"]["count"] > 0:
                        print(f"🔥 ALERT! Fire detected in {img_path.name}")
                        print(f"   Count: {result['data']['count']}")
                        # Send alert (email, SMS, etc)
                    
                    processed.add(img_path)
        
        time.sleep(interval)

# Usage
monitor_folder("./camera_feed", interval=2)
```

### Example 3: Web Integration (Node.js)

```javascript
const express = require('express');
const multer = require('multer');
const FormData = require('form-data');
const fetch = require('node-fetch');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.post('/detect', upload.single('image'), async (req, res) => {
    try {
        const formData = new FormData();
        formData.append('file', fs.createReadStream(req.file.path));
        formData.append('confidence', req.body.confidence || 0.25);
        
        const response = await fetch('http://localhost:8000/api/detect', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        // Cleanup
        fs.unlinkSync(req.file.path);
        
        res.json(result);
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(3000, () => {
    console.log('Proxy server running on port 3000');
});
```

---

## Performance Optimization

### Tips untuk Performa Lebih Baik

1. **Resize Image Before Upload**
   ```python
   from PIL import Image
   
   img = Image.open("large_image.jpg")
   img.thumbnail((640, 640))
   img.save("resized_image.jpg")
   ```

2. **Use GPU for Inference**
   - Pastikan CUDA terinstall
   - PyTorch akan otomatis menggunakan GPU jika tersedia

3. **Batch Processing**
   - Proses multiple images dalam satu session
   - Model hanya di-load sekali

4. **Caching**
   - Cache hasil deteksi untuk gambar yang sama
   - Gunakan hash untuk identifikasi gambar

---

## Security Considerations

### Production Deployment

1. **Add Authentication**
   ```python
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   @app.post("/api/detect")
   async def detect(credentials: HTTPAuthorizationCredentials = Depends(security)):
       # Verify token
       pass
   ```

2. **Enable CORS Properly**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       allow_methods=["POST", "GET"],
   )
   ```

3. **Add Rate Limiting**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/api/detect")
   @limiter.limit("10/minute")
   async def detect():
       pass
   ```

4. **Validate Input**
   - Check file type dan size
   - Sanitize filenames
   - Scan untuk malware

---

## Support

Jika ada pertanyaan atau masalah dengan API, silakan buat issue di repository atau hubungi developer.

---

**Last Updated**: July 2026  
**Version**: 1.0.0
