@echo off
echo ======================================
echo   FIRE DETECTION - YOLOV9 TRAINING
echo ======================================
echo.
echo [INFO] Memulai training model...
echo [INFO] Waktu estimasi: 2-4 jam
echo [INFO] Biarkan komputer menyala
echo [INFO] Tekan Ctrl+C untuk membatalkan
echo.
echo ======================================
echo.

python train_model.py train

echo.
echo ======================================
echo [INFO] Training selesai!
echo [INFO] Tekan tombol apapun untuk keluar...
pause > nul
