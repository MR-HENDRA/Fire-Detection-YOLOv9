# 🔥 Fire Detection - YOLOv9

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![YOLOv9](https://img.shields.io/badge/YOLOv9-E4405F?style=flat-square&logo=pytorch)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Roboflow Dataset](https://img.shields.io/badge/Dataset-Roboflow-Universe-blue)](https://universe.roboflow.com/ltttnt/fire-vqbia)

**Aplikasi deteksi kebakaran real-time menggunakan model YOLOv9 dengan antarmuka web modern**

---

## 📌 Table of Contents

- [📋 About](#-about)
- [✨ Features](#-features)
- [🚀 Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [📁 Project Structure](#-project-structure)
- [🔧 API Documentation](#-api-documentation)
- [📊 Dataset](#-dataset)
- [🛠️ Built With](#-built-with)
- [📈 Performance](#-performance)
- [🎯 Usage](#-usage)
- [🐛 Troubleshooting](#-troubleshooting)
- [🚀 Roadmap](#-roadmap)
- [📝 License](#-license)
- [👤 Author](#-author)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 📋 About

**Fire Detection - YOLOv9** is a real-time fire detection web application that leverages the power of YOLOv9 (You Only Look Once v9) deep learning model. The application allows users to upload images and automatically detect the presence of fire with high accuracy.

### Key Highlights

- **Real-time Detection**: Process images instantly with YOLOv9
- **Web Interface**: Modern, responsive UI with drag & drop upload
- **Adjustable Sensitivity**: Customizable confidence threshold (5% - 95%)
- **Comprehensive Statistics**: Dataset and detection statistics
- **Production Ready**: Built with FastAPI for scalability

---

## ✨ Features

### Core Features
- 🎯 **Real-time Fire Detection**: Upload images and get instant fire detection results
- 🎚️ **Confidence Threshold**: Adjust detection sensitivity from 5% to 95%
- 📊 **Dataset Statistics**: View complete dataset information (train/valid/test splits)
- 🖼️ **Drag & Drop Upload**: Intuitive file upload interface
- 📈 **Detailed Results**: Complete detection table with coordinates and confidence scores
- 🎨 **Modern UI**: Dark theme with glass morphism design

### Technical Features
- **Singleton Model Loading**: Memory-efficient model management
- **Automatic Model Download**: YOLOv9 model downloads on first run
- **CORS Enabled**: Ready for cross-origin requests
- **Error Handling**: Comprehensive error management
- **Responsive Design**: Mobile-friendly interface

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.8+ | Required |
| pip | Latest | Python package manager |
| RAM | 2GB minimum | 4GB recommended |
| GPU | Optional | CUDA enabled for faster inference |

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/MR-HENDRA/Fire-Detection-YOLOv9.git
cd Fire-Detection-YOLOv9
```

2. **Install dependencies**

```bash
pip install -r LOCAL/requirements.txt
```

**Dependencies included:**
- `ultralytics>=8.0.0` - YOLOv9 framework
- `torch>=2.0.0` - PyTorch deep learning
- `torchvision>=0.15.0` - PyTorch computer vision
- `fastapi>=0.95.0` - Web framework
- `uvicorn>=0.21.0` - ASGI server
- `python-multipart>=0.0.6` - File upload support
- `jinja2>=3.1.0` - Template engine

3. **Model Setup**

The YOLOv9c model (`yolov9c.pt`, ~50MB) will be automatically downloaded on first run.

---

## 🎮 Running the Application

### Development Server

```bash
# Method 1: Using Python directly
python app/main.py

# Method 2: Using Uvicorn with auto-reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Server

```bash
# For production (without auto-reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

### Access the Application

Open your browser and navigate to:

```
http://localhost:8000
```

**Available endpoints:**
- **Web Interface**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

---

## 📁 Project Structure

```
A3-HXCODE/
├── app/                          # Main application
│   ├── main.py                   # FastAPI server entry point
│   ├── detector.py               # YOLOv9 detection module
│   ├── static/
│   │   ├── style.css             # Frontend styles
│   │   └── app.js                # Frontend JavaScript
│   └── templates/
│       └── index.html            # Main HTML template
├── GOOGLE_COLAB/                 # Google Colab resources
│   └── colab_fire_detection.ipynb # Training notebook
├── LOCAL/                        # Local development files
│   ├── requirements.txt          # Python dependencies
│   ├── run.bat                   # Windows launcher script
│   ├── start_training.bat        # Training launcher script
│   ├── test_api.py               # API testing script
│   └── train_model.py            # Model training script
├── DOCUMENTATION/                # Project documentation
│   ├── README.md                 # This file
│   ├── API_DOCUMENTATION.md      # API endpoints documentation
│   ├── CHANGELOG.md              # Version history
│   └── DEPLOYMENT.md             # Deployment guides
├── .gitignore                    # Git ignore rules
└── README.md                     # Repository root README
```

---

## 🔧 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web interface |
| POST | `/api/detect` | Detect fire in uploaded image |
| GET | `/api/dataset-stats` | Get dataset statistics |

### Detect Fire Endpoint

**Request:**
```bash
POST /api/detect
Content-Type: multipart/form-data
```

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file` | UploadFile | Yes | - | Image file to detect |
| `confidence` | float | No | 0.25 | Confidence threshold (0.0 - 1.0) |

**Supported Formats:** JPG, PNG, WEBP, BMP, TIFF
**Max File Size:** 10MB

**Response:**
```json
{
  "success": true,
  "data": {
    "annotated_image_base64": "base64_encoded_image",
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

### Dataset Statistics Endpoint

**Request:**
```bash
GET /api/dataset-stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "train": {"images": 4000, "labels": 4000},
    "valid": {"images": 1000, "labels": 1000},
    "test": {"images": 710, "labels": 710}
  }
}
```

For complete API documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 📊 Dataset

### Dataset Information

| Property | Value |
|----------|-------|
| **Source** | [Roboflow Universe - Fire Detection](https://universe.roboflow.com/ltttnt/fire-vqbia) |
| **License** | CC BY 4.0 |
| **Total Images** | 5,710 |
| **Classes** | 1 (Fire) |
| **Resolution** | 640 × 640 pixels |
| **Format** | YOLO format |

### Dataset Split

| Split | Images | Labels | Percentage |
|-------|--------|--------|------------|
| Train | 4,808 | 4,808 | ~84% |
| Validation | 601 | 601 | ~11% |
| Test | 301 | 301 | ~5% |

---

## 🛠️ Built With

### Backend
- **[Python 3.8+](https://www.python.org/)** - Programming language
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework
- **[Ultralytics YOLOv9](https://github.com/ultralytics/ultralytics)** - Object detection framework
- **[PyTorch](https://pytorch.org/)** - Deep learning framework
- **[Pillow (PIL)](https://python-pillow.org/)** - Image processing

### Frontend
- **[HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML)** - Page structure
- **[CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)** - Styling with glass morphism
- **[JavaScript (ES6+)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)** - Frontend logic
- **[Google Fonts - Inter](https://fonts.google.com/specimen/Inter)** - Typography

### Model Architecture
- **Model**: YOLOv9c (Compact version)
- **Input Size**: 640 × 640 pixels
- **Classes**: 1 (Fire)
- **Architecture**: CSPNet + PAN + Detection Head
- **Pretrained**: COCO dataset (80 classes)

---

## 📈 Performance

| Metric | Value | Notes |
|--------|-------|-------|
| **Inference Time** | 0.5 - 2 seconds | Depends on hardware |
| **Accuracy** | 85-95% | Depends on confidence threshold |
| **Model Size** | ~50MB | yolov9c.pt |
| **Memory Usage** | ~2GB RAM | During inference |
| **GPU Acceleration** | Supported | CUDA enabled |

---

## 🎯 Usage

### Step-by-Step Guide

1. **Upload Image**
   - Click the upload area or drag & drop an image
   - Supported formats: JPG, PNG, WEBP
   - Maximum size: 10MB

2. **Adjust Confidence Threshold**
   - Use the slider to set sensitivity
   - **5% - 50%**: More sensitive, detects more (may have false positives)
   - **50% - 95%**: More accurate, only detects with high confidence

3. **Start Detection**
   - Click "Mulai Deteksi" button
   - Wait for AI processing (usually 1-3 seconds)

4. **View Results**
   - Annotated image with bounding boxes
   - Fire count statistics
   - Detailed table with coordinates and confidence scores

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **Model not found** | Model downloads automatically on first run. Ensure internet connection |
| **Module not found** | Reinstall dependencies: `pip install -r LOCAL/requirements.txt --upgrade` |
| **Port already in use** | Find and kill process: `netstat -ano \| findstr :8000` then `taskkill /PID <PID> /F` |
| **Slow detection** | Use GPU (CUDA), reduce image resolution, or use smaller model (yolov9n.pt) |
| **False positives** | Increase confidence threshold (move slider right) |
| **Fire not detected** | Decrease confidence threshold (move slider left) |

### Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 500 | Internal Server Error - Server-side issue |

---

## 🚀 Roadmap

### Planned Features

- [ ] **Video Detection** - Real-time video fire detection
- [ ] **Webcam Integration** - Live detection from webcam
- [ ] **Alert System** - Email/SMS/webhook notifications
- [ ] **Multi-class Detection** - Detect smoke, flames, etc.
- [ ] **Export Results** - Download detection results (JSON/CSV)
- [ ] **Batch Processing** - Process multiple images at once
- [ ] **Mobile Optimization** - Better mobile device support
- [ ] **Theme Toggle** - Dark/Light theme switch
- [ ] **Detection History** - Save and view detection history
- [ ] **Custom Training UI** - Web interface for model training

### Training Custom Model

```bash
# Install ultralytics
pip install ultralytics

# Train using provided script
python LOCAL/train_model.py train

# Or use Google Colab
# Open GOOGLE_COLAB/colab_fire_detection.ipynb
```

---

## 📝 License

This project is open source and available under the following licenses:

| Component | License | Link |
|-----------|---------|------|
| **Code** | MIT License | [LICENSE](https://opensource.org/licenses/MIT) |
| **Dataset** | CC BY 4.0 | [Creative Commons](https://creativecommons.org/licenses/by/4.0/) |
| **YOLOv9 Model** | GPL-3.0 | [Ultralytics License](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) |

---

## 👤 Author

**Hendra**
- **Project**: A3-HXCODE
- **Year**: 2026
- **GitHub**: [MR-HENDRA](https://github.com/MR-HENDRA)

---

## 🙏 Acknowledgments

- **[Ultralytics](https://github.com/ultralytics/ultralytics)** - YOLOv9 framework
- **[Roboflow Universe](https://universe.roboflow.com/)** - Dataset provider
- **[FastAPI](https://fastapi.tiangolo.com/)** - Web framework
- **[Dataset by ltttnt](https://universe.roboflow.com/ltttnt/fire-vqbia)** - Fire detection dataset
- **[GitHub Repository](https://github.com/MR-HENDRA/Fire-Detection-YOLOv9)** - Project source code

---

**🔥 Stay Safe! Detect Fire Early with AI 🔥**

*For questions or issues, please create an issue in the repository or contact the author.*