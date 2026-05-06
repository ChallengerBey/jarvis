import subprocess
import sys

def install_packages():
    # JARVIS Flask Server paketleri
    jarvis_packages = [
        "flask",
        "flask-cors",
        "pyautogui",
        "psutil",
        "requests",
        "numpy",
        "pyaudio",
        "piper-tts",
        "pywebview",
        "pygame"
    ]
    
    # Hand Tracking paketleri
    hand_tracking_packages = [
        "opencv-python==4.8.1.78",
        "mediapipe==0.10.8",
        "pyautogui==0.9.54"
    ]

    print("=" * 60)
    print("[*] J.A.R.V.I.S + HAND TRACKING Dependency Installer")
    print("=" * 60)
    print()
    
    # JARVIS paketleri
    print("[1/2] Installing JARVIS packages...")
    print("-" * 60)
    for package in jarvis_packages:
        print(f"[*] Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"[+] Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"[-] Failed to install {package}. You might need to install it manually.")
            if package == "pyaudio":
                print("    Hint: For PyAudio, you might need to download a .whl file if you don't have C++ Build Tools.")
    
    print()
    
    # Hand Tracking paketleri
    print("[2/2] Installing Hand Tracking packages...")
    print("-" * 60)
    for package in hand_tracking_packages:
        print(f"[*] Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"[+] Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"[-] Failed to install {package}.")

    print()
    print("=" * 60)
    print("[!] All installation attempts finished.")
    print()
    print("Next steps:")
    print("  1. Test camera: python test_camera.py")
    print("  2. Test hand tracking: python hand_tracking_debug.py")
    print("  3. Start JARVIS: python jarvis_app.py")
    print("  4. Start web: npm run dev")
    print("=" * 60)

if __name__ == "__main__":
    install_packages()
