# JARVIS Desktop Assistant

AI-powered desktop assistant with voice (Piper TTS), hand tracking (MediaPipe/TensorFlow), and system control. Built with **Next.js 15** (React 19) + **Flask/Python** backend.

## Features

- **Voice Interface** — Piper TTS (offline, ONNX) + clap detection activation
- **Hand Tracking** — MediaPipe Hands / TensorFlow.js for gesture control
- **System Control** — Open apps, lock workstation, media keys, system stats
- **Web UI** — Next.js + Three.js (React Three Fiber) frontend served via Flask
- **Desktop App** — PyWebView wrapper for native window

## Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js 15, React 19, Tailwind 4, Three.js (R3F) |
| Backend | Flask, pywebview, Piper TTS, MediaPipe, OpenCV |
| Voice | Piper (ONNX), PyAudio for clap detection |
| Tracking | @mediapipe/hands, @tensorflow-models/hand-pose-detection |

## Quick Start

```bash
# Install Python deps
pip install -r requirements_hand.txt
pip install flask flask-cors psutil pyautogui pyaudio piper-tts opencv-python mediapipe numpy

# Install Node deps
npm install

# Build Next.js for Flask to serve
npm run build

# Run desktop app
python jarvis_app.py
```

## Project Structure

```
jarvis/
├── app/                    # Next.js 15 app (React frontend)
├── lib/                    # Shared utilities
├── models/                 # Piper ONNX voice models
├── public/                 # Static assets
├── Sound/                  # Audio files
├── jarvis_app.py           # Main entry: Flask + PyWebView + TTS + clap detection
├── flask_server.py         # Alternative Flask server
├── hand_tracking_debug.py  # Hand tracking debugging
├── test_camera.py          # Camera testing
├── sinek_oyunu.py          # Fly swatter game (hand tracking demo)
├── yilan_oyunu.py          # Snake game (hand tracking demo)
├── package.json            # Node dependencies
└── requirements_hand.txt   # Python dependencies
```

## Commands (via Web UI)

- `open_program` — Launch app or open URL
- `system_status` — CPU/RAM usage
- `lock_workstation` — Lock screen
- `media_control` — Volume up/down/mute
- `execute_macro` — Preset workflows (e.g., "work" mode)
- `type_text` — Simulate typing

## License

MIT

## Author

**Semih Ergili** — [@ChallengerBey](https://github.com/ChallengerBey)