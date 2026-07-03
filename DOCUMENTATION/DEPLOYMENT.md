# 🚀 Deployment Guide - Fire Detection YOLOv9

Panduan lengkap untuk melakukan deployment aplikasi Fire Detection ke berbagai platform.

## 📋 Daftar Isi

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
  - [Docker](#docker)
  - [Linux Server](#linux-server)
  - [Windows Server](#windows-server)
  - [Cloud Platforms](#cloud-platforms)
- [Configuration](#configuration)
- [Security](#security)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 10GB free space
- **OS**: Windows 10+, Ubuntu 18.04+, macOS 10.15+
- **Python**: 3.8 or higher

### Recommended for Production
- **CPU**: 4+ cores
- **RAM**: 8GB+
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster inference)
- **Storage**: 20GB+ SSD
- **OS**: Ubuntu 20.04 LTS or higher

---

## Local Development

### 1. Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd A3-HXCODE

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Development Server

```bash
# Simple way
python app/main.py

# Or with uvicorn (with auto-reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Access Application

```
http://localhost:8000
```

---

## Production Deployment

### Docker Deployment

#### 1. Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY "FIRE DETECTION USING YOLOV9/" ./"FIRE DETECTION USING YOLOV9"/

# Download YOLOv9 model
RUN python -c "from ultralytics import YOLO; YOLO('yolov9c.pt')"

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Create docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  fire-detection:
    build: .
    container_name: fire-detection-app
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app
      - ./uploads:/app/uploads
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - DEBUG=False
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

#### 3. Build and Run

```bash
# Build image
docker build -t fire-detection:latest .

# Run container
docker run -d \
  --name fire-detection \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  fire-detection:latest

# Or use docker-compose
docker-compose up -d
```

#### 4. View Logs

```bash
docker logs -f fire-detection
```

---

### Linux Server Deployment

#### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install system dependencies
sudo apt install libgl1-mesa-glx libglib2.0-0 -y
```

#### 2. Setup Application

```bash
# Create app directory
sudo mkdir -p /opt/fire-detection
cd /opt/fire-detection

# Upload application files (use scp, rsync, or git)
git clone <repository-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Create Systemd Service

```bash
sudo nano /etc/systemd/system/fire-detection.service
```

```ini
[Unit]
Description=Fire Detection API Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/fire-detection
Environment="PATH=/opt/fire-detection/venv/bin"
ExecStart=/opt/fire-detection/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### 4. Start Service

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable fire-detection

# Start service
sudo systemctl start fire-detection

# Check status
sudo systemctl status fire-detection
```

#### 5. Setup Nginx Reverse Proxy

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/fire-detection
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/fire-detection /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

#### 6. Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

### Windows Server Deployment

#### 1. Install Python

Download and install Python 3.10+ from python.org

#### 2. Setup Application

```cmd
cd C:\inetpub\fire-detection

# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Install as Windows Service

Install NSSM (Non-Sucking Service Manager):

```cmd
# Download NSSM from nssm.cc
# Extract and add to PATH

# Install service
nssm install FireDetection "C:\inetpub\fire-detection\venv\Scripts\python.exe" "C:\inetpub\fire-detection\venv\Scripts\uvicorn.exe app.main:app --host 0.0.0.0 --port 8000"

# Set startup directory
nssm set FireDetection AppDirectory "C:\inetpub\fire-detection"

# Start service
nssm start FireDetection
```

---

### Cloud Platforms

#### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu 20.04, t3.medium or larger)
# 2. SSH to instance
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com

# 3. Follow Linux Server Deployment steps above

# 4. Configure Security Group to allow port 80 and 443
```

#### Google Cloud Platform

```bash
# 1. Create Compute Engine instance
gcloud compute instances create fire-detection \
  --machine-type=n1-standard-2 \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud

# 2. SSH to instance
gcloud compute ssh fire-detection

# 3. Follow Linux Server Deployment steps
```

#### Azure

```bash
# 1. Create VM (Ubuntu 20.04, Standard B2s or larger)
az vm create \
  --resource-group myResourceGroup \
  --name fire-detection \
  --image UbuntuLTS \
  --size Standard_B2s

# 2. SSH to VM
ssh azureuser@<public-ip>

# 3. Follow Linux Server Deployment steps
```

#### Heroku

```bash
# 1. Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 2. Create runtime.txt
echo "python-3.10.12" > runtime.txt

# 3. Deploy
heroku create fire-detection-app
git push heroku main
```

#### Railway / Render

1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Deploy

---

## Configuration

### Environment Variables

Create `.env` file:

```bash
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Model
MODEL_PATH=yolov9c.pt
MODEL_CONF_THRESHOLD=0.25

# Security
SECRET_KEY=your-secret-key-here
API_KEY_ENABLED=True
API_KEY=your-api-key

# CORS
CORS_ORIGINS=https://yourdomain.com
```

### Load Environment Variables

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    model_path: str = "yolov9c.pt"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Security

### 1. Enable HTTPS

Always use HTTPS in production. Use Let's Encrypt for free SSL certificates.

### 2. Add Authentication

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security, HTTPException

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != "your-secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials

@app.post("/api/detect")
async def detect(token: str = Depends(verify_token)):
    # Your code here
    pass
```

### 3. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/detect")
@limiter.limit("10/minute")
async def detect(request: Request):
    pass
```

### 4. Input Validation

```python
from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def validate_image(file: UploadFile):
    # Check file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid file type")
    
    # Check file size
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    
    if size > MAX_FILE_SIZE:
        raise HTTPException(400, "File too large")
```

---

## Monitoring

### 1. Application Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 2. Performance Monitoring

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"{request.method} {request.url.path} - {process_time:.2f}s")
    return response
```

### 3. Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": _model is not None
    }
```

---

## Troubleshooting

### Issue: Model not loading

**Solution:**
```bash
# Manually download model
python -c "from ultralytics import YOLO; YOLO('yolov9c.pt')"
```

### Issue: Out of memory

**Solution:**
- Use smaller model (yolov9n.pt)
- Reduce batch size
- Add swap space
- Upgrade RAM

### Issue: Slow inference

**Solution:**
- Enable GPU acceleration
- Use ONNX export
- Reduce image resolution
- Use model quantization

### Issue: Port already in use

**Solution:**
```bash
# Find process
netstat -tulpn | grep 8000

# Kill process
kill -9 <PID>
```

---

## Backup and Recovery

### Backup Model and Data

```bash
# Backup script
tar -czf backup-$(date +%Y%m%d).tar.gz \
  app/ \
  "FIRE DETECTION USING YOLOV9/" \
  requirements.txt \
  README.md
```

### Restore

```bash
tar -xzf backup-20260702.tar.gz
```

---

## Performance Tuning

### 1. Enable GPU

```python
# Check CUDA availability
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
```

### 2. Use Multiple Workers

```bash
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### 3. Enable Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_detection(image_hash):
    # Your detection logic
    pass
```

---

## Maintenance

### Update Dependencies

```bash
# Update pip
pip install --upgrade pip

# Update packages
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip-audit
```

### Rotate Logs

```bash
# /etc/logrotate.d/fire-detection
/var/log/fire-detection/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## Support

For deployment issues:
1. Check logs: `docker logs fire-detection` or `sudo journalctl -u fire-detection`
2. Review this guide
3. Check GitHub issues
4. Contact support

---

**Last Updated**: July 2026  
**Version**: 1.0.0
