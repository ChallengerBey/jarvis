@echo off
echo ========================================
echo    HAND TRACKING DEBUG TOOL
echo ========================================
echo.

echo [1/2] Paketler kuruluyor...
pip install -r requirements_hand.txt

echo.
echo [2/2] Hand tracking baslatiliyor...
echo.
python hand_tracking_debug.py

pause
