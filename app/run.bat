@echo off
:: ========================================
:: Fire Detection - YOLOv9 Launcher Script
:: ========================================

echo.
echo ========================================
echo   Fire Detection - YOLOv9
echo   Starting Application...
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python 3.8+ dari https://www.python.org/
    pause
    exit /b 1
)

:: Check if requirements are installed
echo [INFO] Memeriksa dependencies...
python -c "import fastapi, uvicorn, ultralytics" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Dependencies belum terinstall lengkap.
    echo [INFO] Menginstall dependencies...
    pip install -r app/requirements.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Gagal menginstall dependencies!
        pause
        exit /b 1
    )
)

echo [INFO] Dependencies OK!
echo.
echo ========================================
echo   Menjalankan Server...
echo ========================================
echo.
echo ^> Buka browser dan akses:
echo   http://localhost:8000
echo.
echo ^> Tekan Ctrl+C untuk menghentikan server
echo.
echo ========================================
echo.

:: Run the application
python app/main.py

pause
