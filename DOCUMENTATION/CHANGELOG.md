# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-07-02

### 📦 Added

#### Core Features

- ✨ Initial release of Fire Detection application using YOLOv9
- 🎯 YOLOv9-based fire detection system with real-time processing
- 🌐 FastAPI backend server with RESTful API endpoints
- 🎨 Modern web interface with dark theme and glass morphism design
- 📤 Drag & drop file upload functionality with image preview
- 🎚️ Adjustable confidence threshold slider (5% - 95%)
- 📊 Real-time detection statistics display
- 📈 Dataset statistics viewer (train/valid/test splits)
- 🖼️ Annotated image output with bounding boxes
- 📋 Detailed detection table with coordinates and confidence scores

#### Infrastructure

- 📦 Dependency management via `LOCAL/requirements.txt`
- 🚀 One-click launcher script (`LOCAL/run.bat`)
- 🏋️ Model training script with validation (`LOCAL/train_model.py`)
- 🧪 Automated API testing script (`LOCAL/test_api.py`)
- ⚙️ Environment configuration template (`.env.example`)
- 🔒 `.gitignore` for Python projects

#### Documentation

- 📖 Complete README with installation and usage guide
- 📚 Comprehensive API documentation (`API_DOCUMENTATION.md`)
- 📝 Version history tracking (`CHANGELOG.md`)
- 🚀 Deployment guides (`DEPLOYMENT.md`)
- 📓 Google Colab training notebook (`GOOGLE_COLAB/colab_fire_detection.ipynb`)

#### Dataset

- 🔥 5,710 labeled fire detection images from Roboflow Universe
- 📊 Dataset split: 4,808 train (~84%), 601 validation (~11%), 301 test (~5%)
- 🎯 Single class: Fire
- 📐 Resolution: 640 × 640 pixels
- 📜 CC BY 4.0 license

### 🎨 Features

#### Backend (FastAPI)

- Automatic API documentation via Swagger UI (`/docs`) and ReDoc (`/redoc`)
- Singleton pattern for memory-efficient model loading
- Multi-part form data support for file uploads
- JSON API responses with proper error handling
- CORS enabled for cross-origin requests
- Async/await support for better performance

#### Frontend

- Responsive design (mobile-friendly)
- Tab-based navigation (Detection, Dataset, About)
- Image preview before detection
- Real-time result visualization with animated transitions
- Loading states and progress indicators
- Re-upload capability by clicking preview
- Smooth CSS transitions and animations

#### AI Model (YOLOv9)

- YOLOv9c (compact version) for balance of speed and accuracy
- Automatic model download on first run (~50MB)
- Adjustable confidence threshold (0.0 - 1.0)
- Bounding box visualization with fire-themed colors (red/orange)
- Multiple fire detection support in single image
- GPU acceleration support (CUDA)

### 🔧 Technical Details

| Component         | Technology         | Version           |
| ----------------- | ------------------ | ----------------- |
| **Language**      | Python             | 3.8+              |
| **Web Framework** | FastAPI            | >=0.95.0          |
| **DL Framework**  | PyTorch            | >=2.0.0           |
| **Model**         | Ultralytics YOLOv9 | >=8.0.0           |
| **Templates**     | Jinja2             | >=3.1.0           |
| **Frontend**      | Vanilla JavaScript | ES6+              |
| **Styling**       | CSS3               | Custom Properties |
| **Fonts**         | Google Fonts       | Inter             |

### 📚 Documentation

- README.md with complete setup and usage guide
- API_DOCUMENTATION.md with endpoint details, examples, and integration guides
- Inline code comments in Indonesian and English
- Example integration code (Python, JavaScript, Node.js)
- Troubleshooting section with common issues
- Performance optimization tips and best practices

### ⚠️ Known Limitations

- Single class detection (fire only)
- Image-only detection (no video/webcam support yet)
- No authentication/authorization system
- No rate limiting implemented
- No caching mechanism
- Model download required on first run (~50MB)

### 🎯 Future Enhancements

- [ ] Video and webcam real-time detection
- [ ] Multi-class detection (smoke, flames, etc.)
- [ ] Alert system (email, SMS, webhook notifications)
- [ ] Batch processing for multiple images
- [ ] Detection history and export functionality
- [ ] Custom model training UI
- [ ] Docker containerization
- [ ] Cloud deployment guides (AWS, GCP, Azure)
- [ ] Mobile app (React Native)
- [ ] Authentication and API keys system

---

## 📋 Release Notes

### v1.0.0 - Initial Release

This is the **first stable release** of the Fire Detection application using YOLOv9.
The application is fully functional and production-ready for:

- 🎓 **Educational purposes** - Learn about YOLOv9 and fire detection
- 🧪 **Research and experimentation** - Test different configurations
- 🔬 **Proof of concept demonstrations** - Showcase AI capabilities
- 🏗️ **Foundation for production systems** - Build upon for real-world deployment

### System Requirements

| Requirement | Minimum                 | Recommended         |
| ----------- | ----------------------- | ------------------- |
| **Python**  | 3.8                     | 3.10+               |
| **RAM**     | 2GB                     | 4GB+                |
| **Storage** | 10GB                    | 20GB SSD            |
| **GPU**     | -                       | NVIDIA CUDA-enabled |
| **OS**      | Windows 10+/Linux/macOS | Ubuntu 20.04 LTS    |

### Quick Start Guide

```bash
# 1. Clone the repository
git clone https://github.com/MR-HENDRA/Fire-Detection-YOLOv9.git
cd Fire-Detection-YOLOv9

# 2. Install dependencies
pip install -r LOCAL/requirements.txt

# 3. Run the server
python app/main.py

# 4. Open in browser
# Navigate to http://localhost:8000
```

### Usage Steps

1. Install dependencies
2. Run the server
3. Open `http://localhost:8000` in browser
4. Upload an image (drag & drop or click)
5. Adjust confidence threshold (optional)
6. Click "Mulai Deteksi"
7. View results with bounding boxes

---

## 📖 Project Structure

```
A3-HXCODE/
├── app/                          # Main application directory
│   ├── main.py                   # FastAPI server entry point
│   ├── detector.py               # YOLOv9 detection logic
│   ├── static/
│   │   ├── style.css             # Frontend CSS styles
│   │   └── app.js                # Frontend JavaScript
│   └── templates/
│       └── index.html            # Main HTML template
├── GOOGLE_COLAB/                 # Google Colab resources
│   └── colab_fire_detection.ipynb # Jupyter notebook for training
├── LOCAL/                        # Local development files
│   ├── requirements.txt          # Python package dependencies
│   ├── run.bat                   # Windows batch file to run server
│   ├── start_training.bat        # Windows batch file for training
│   ├── test_api.py               # API testing and validation script
│   └── train_model.py            # Model training script
├── DOCUMENTATION/                # Project documentation
│   ├── README.md                 # Main documentation file
│   ├── API_DOCUMENTATION.md      # API endpoints documentation
│   ├── CHANGELOG.md              # This file - version history
│   └── DEPLOYMENT.md             # Deployment guides
├── .gitignore                    # Git ignore rules
└── README.md                     # Repository root README
```

---

## 🤝 Contributing

We welcome contributions! To contribute to this project:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** thoroughly
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Submit** a Pull Request

### Contribution Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits atomic and well-described

---

## 📜 License

This project uses multiple licenses:

| Component        | License     | License File                                                                        |
| ---------------- | ----------- | ----------------------------------------------------------------------------------- |
| **Source Code**  | MIT License | [MIT](https://opensource.org/licenses/MIT)                                          |
| **Dataset**      | CC BY 4.0   | [Creative Commons](https://creativecommons.org/licenses/by/4.0/)                    |
| **YOLOv9 Model** | GPL-3.0     | [Ultralytics License](https://github.com/ultralytics/ultralytics/blob/main/LICENSE) |

---

## 👤 Author & Maintainer

**Hendra**

- **GitHub**: [@MR-HENDRA](https://github.com/MR-HENDRA)
- **Project**: A3-HXCODE
- **Year**: 2026
- **Email**: (available in GitHub profile)

---

## 📅 Version History

| Version | Date       | Description            |
| ------- | ---------- | ---------------------- |
| 1.0.0   | 2026-07-02 | Initial stable release |

---

**📌 Note**: This changelog follows the [Keep a Changelog](https://keepachangelog.com/) format.
**🔗 Links**:

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

_Last Updated: 2026-07-04_
_Format: Markdown_
_Style: Professional, Structured, Industry Standard_
