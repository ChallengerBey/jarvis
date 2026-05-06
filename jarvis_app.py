import os
import sys
import subprocess
import threading
import time
import json
import pyautogui
import winsound
import io
import psutil
import requests
import numpy as np
import traceback
import random
import pyaudio
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from piper.voice import PiperVoice

# --- PYWEBVIEW KONTROL ---
try:
    import webview
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywebview"])
    import webview

app = Flask(__name__, static_folder='out', static_url_path='')
CORS(app)

HAFIZA_DOSYASI = "haci_hafiza.json"
MODEL_PATH = "models/en_US-john-medium.onnx"
voice = None

print("[!] JARVIS Voice Model loading...")
try:
    voice = PiperVoice.load(MODEL_PATH)
    print("[+] Voice model ready!")
except Exception as e:
    print(f"[-] Model failed: {e}")

def jarvis_konus(metin):
    if not voice: 
        print("[-] Ses modeli yuklu degil!")
        return
    filename = f"output_{random.randint(1000,9999)}.wav"
    try:
        print(f"[*] Jarvis konusuyor: {metin}")
        import wave
        with wave.open(filename, "wb") as wav_file:
            voice.synthesize_wav(metin, wav_file)
        
        # Sesi çal
        winsound.PlaySound(filename, winsound.SND_FILENAME)
        
    except Exception as e:
        print(f"[-] TTS Calma Hatasi: {e}")
    finally:
        # Dosyayı her durumda temizle
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"[*] Dosya temizlendi: {filename}")
            except:
                pass

@app.route('/')
def serve_index():
    return send_from_directory('out', 'index.html')

@app.route('/_next/<path:path>')
def serve_next(path):
    return send_from_directory('out/_next', path)

@app.route('/<path:path>')
def serve_static(path):
    full_path = os.path.join('out', path)
    if os.path.exists(full_path):
        return send_from_directory('out', path)
    return send_from_directory('out', 'index.html')

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json(silent=True) or {}
    action = data.get('action')
    args = data.get('args', {})
    print(f"[x] Command received: {action}")

    try:
        if action == "open_program":
            prog = args.get("name", "")
            if prog.lower().startswith("http"):
                import webbrowser
                webbrowser.open(prog)
            else:
                pyautogui.press("win")
                time.sleep(1)
                pyautogui.write(prog, interval=0.1)
                time.sleep(0.5)
                pyautogui.press("enter")
            return jsonify({"status": "success", "message": f"{prog} started."})

        elif action == "system_status":
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            return jsonify({"status": "success", "message": f"Systems nominal. CPU: {cpu}%, RAM: {ram}%. Arc Reactor stable."})

        elif action == "lock_workstation":
            import ctypes
            ctypes.windll.user32.LockWorkStation()
            return jsonify({"status": "success", "message": "Secured."})

        elif action == "media_control":
            cmd = args.get("command", "")
            if cmd == "volume_up": pyautogui.press("volumeup")
            elif cmd == "volume_down": pyautogui.press("volumedown")
            elif cmd == "mute": pyautogui.press("volumemute")
            return jsonify({"status": "success"})

        elif action == "execute_macro":
            profile = args.get("profile", "")
            if profile == "work":
                import webbrowser
                webbrowser.open("https://gemini.google.com")
                time.sleep(0.5)
                webbrowser.open("https://www.youtube.com/watch?v=XMEXPkPmmq0&list=RDXMEXPkPmmq0&start_radio=1") 
                return jsonify({"status": "success", "message": "Work mode active."})

        elif action == "type_text":
            pyautogui.write(args.get("text", ""), interval=0.01)
            return jsonify({"status": "success"})

        return jsonify({"status": "success", "message": "Done."})
    except Exception as e:
        print(f"[-] Execution Error: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    metin = data.get('text', '')
    # Ses işlemini ayrı thread'de yap ki UI donmasın
    threading.Thread(target=jarvis_konus, args=(metin,), daemon=True).start()
    return jsonify({"status": "success"})

def alkis_dinle():
    CHUNK, RATE, THRESHOLD = 1024, 44100, 15000 # Esik 15000'e dusuruldu
    p_in = pyaudio.PyAudio()
    try:
        stream = p_in.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print(f"[*] Alkis Sensoru Aktif... (Esik: {THRESHOLD})")
        while True:
            try:
                data_raw = stream.read(CHUNK, exception_on_overflow=False)
                data = np.frombuffer(data_raw, dtype=np.int16)
                peak = np.max(np.abs(data))
                if peak > THRESHOLD:
                    print(f"[!] Alkis algilandi! Seviye: {peak}")
                    threading.Thread(target=jarvis_konus, args=("Buyrun efendim, sizi dinliyorum.",), daemon=True).start()
                    time.sleep(1.5) # Ust uste tetiklenmeyi onle
            except Exception as e:
                print(f"[-] Mikrofon Okuma Hatasi: {e}")
                time.sleep(1)
    except Exception as e:
        print(f"[-] Alkis Sensoru Baslatilamadi: {e}")

if __name__ == '__main__':
    # Eski dosyalari temizle
    print("[*] Temizlik yapiliyor...")
    for f in os.listdir('.'):
        if f.startswith("output_") and f.endswith(".wav"):
            try: os.remove(f)
            except: pass

    # Flask sunucusunu baslat
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, use_reloader=False), daemon=True).start()
    
    # Alkis dinlemeyi baslat
    threading.Thread(target=alkis_dinle, daemon=True).start()
    
    print("[*] Launching J.A.R.V.I.S Desktop App...")
    time.sleep(1)
    webview.create_window('J.A.R.V.I.S CORE', 'http://127.0.0.1:8080', width=1300, height=900)
    webview.start()
