# Changelog

All notable changes to the Fire Detection YOLOv9 project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2026-07-02

### Added
- ✨ Initial release of Fire Detection application
- 🎯 YOLOv9-based fire detection system
- 🌐 FastAPI backend server with REST API
- 🎨 Modern web interface with dark theme and glass morphism
- 📤 Drag & drop file upload functionality
- 🎚️ Adjustable confidence threshold slider (5% - 95%)
- 📊 Real-time detection statistics display
- 📈 Dataset statistics viewer (train/valid/test splits)
- 🖼️ Annotated image output with bounding boxes
- 📋 Detailed detection table with coordinates and confidence
- 🔥 5710 training images from Roboflow Universe
- 📚 Comprehensive API documentation
- 🧪 Automated API testing script (`LOCAL/test_api.py`)
- 🚀 One-click launcher script (`LOCAL/run.bat`)
- 🏋️ Model training script with validation (`LOCAL/train_model.py`)
- ⚙️ Environment configuration template
- 📖 Complete README with installation guide
- 🔒 .gitignore for Python projects
- 📓 Google Colab training notebook (`GOOGLE_COLAB/colab_fire_detection.ipynb`)

### Features
- **Backend**:
  - FastAPI server with automatic API documentation (Swagger UI)
  - Singleton pattern for model loading (memory efficient)
  - Multi-part form data support for file uploads
  - JSON API responses with proper error handling
  - CORS enabled for cross-origin requests

- **Frontend**:
  - Responsive design (mobile-friendly)
  - Tab-based navigation (Detection, Dataset, About)
  - Image preview before detection
  - Real-time result visualization
  - Animated UI elements with smooth transitions
  - Loading states and progress indicators
  - Re-upload capability by clicking preview

- **AI Model**:
  - YOLOv9c (compact version) for balance of speed and accuracy
  - Automatic model download on first run
  - Adjustable confidence threshold
  - Bounding box visualization with fire-themed colors
  - Multiple fire detection support

- **Dataset**:
  - 5710 labeled images
  - Train/Valid/Test split (~70/20/10)
  - 640x640 pixel resolution
  - Single class: Fire
  - CC BY 4.0 license

### Technical Details
- Python 3.8+ compatible
- PyTorch-based deep learning
- PIL for image processing
- Jinja2 templating engine
- Vanilla JavaScript (no framework dependencies)
- CSS3 with custom properties (CSS variables)
- Google Fonts (Inter typeface)

### Documentation
- README.md with complete setup guide
- API_DOCUMENTATION.md with endpoint details and examples
- DEPLOYMENT.md with production deployment guides
- Inline code comments in Indonesian and English
- Example integration code (Python, JavaScript, Node.js)
- Troubleshooting section
- Performance optimization tips

### Known Limitations
- Single class detection (fire only)
- Image-only detection (no video/webcam support yet)
- No authentication/authorization
- No rate limiting
- No caching mechanism
- Model download required on first run (~50MB)

### Future Enhancements (Planned)
- [ ] Video and webcam real-time detection
- [ ] Multi-class detection (smoke, flames, etc.)
- [ ] Alert system (email, SMS, webhook)
- [ ] Batch processing for multiple images
- [ ] Detection history and export
- [ ] Custom model training UI
- [ ] Docker containerization
- [ ] Cloud deployment guides
- [ ] Mobile app (React Native)
- [ ] Authentication and API keys

---

## Release Notes

### v1.0.0 - Initial Release

This is the first stable release of the Fire Detection application using YOLOv9. The application is fully functional and ready for:

- 🎓 Educational purposes
- 🧪 Research and experimentation
- 🔬 Proof of concept demonstrations
- 🏗️ Foundation for production systems

**System Requirements:**
- Python 3.8 or higher
- 2GB RAM minimum (4GB recommended)
- GPU optional but recommended for faster inference
- Windows/Linux/macOS compatible

**Installation:**
```bash
pip install -r LOCAL/requirements.txt
python app/main.py
```

**Quick Start:**
1. Install dependencies
2. Run the server
3. Open http://localhost:8000 in browser
4. Upload an image
5. Adjust confidence threshold
6. Click "Mulai Deteksi"

---

## Project Structure

```
A3-HXCODE/
├── app/
│   ├── main.py              # FastAPI server
│   ├── detector.py          # YOLOv9 detection module
│   ├── static/
│   │   ├── style.css        # Frontend styling
│   │   └── app.js           # Frontend logic
│   └── templates/
│       └── index.html       # Main page
├── GOOGLE_COLAB/
│   └── colab_fire_detection.ipynb  # Training notebook
├── LOCAL/
│   ├── requirements.txt     # Python dependencies
│   ├── run.bat              # Windows launcher
│   ├── start_training.bat   # Training launcher
│   ├── test_api.py          # API testing script
│   └── train_model.py       # Model training script
└── DOCUMENTATION/
    ├── README.md            # Main documentation
    ├── API_DOCUMENTATION.md # API endpoints
    ├── CHANGELOG.md         # This file
    └── DEPLOYMENT.md        # Deployment guides
```

---

## Contributing

If you'd like to contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## License

- Code: MIT License
- Dataset: CC BY 4.0
- Model: Ultralytics YOLOv9 (GPL-3.0)

---

**Author**: Hendra
**Project**: A3-HXCODE
**Date**: July 2026
**Last Updated**: 2026-07-04