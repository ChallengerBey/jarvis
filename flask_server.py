import os
import time
import json
import pyautogui
import psutil
import numpy as np
import threading
import pyaudio
import webbrowser
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from piper.voice import PiperVoice
from pygame import mixer

app = Flask(__name__)
CORS(app)

# Pygame mixer'ı başlat
mixer.init()

# Global state for clap detection
clap_detected_flag = False

MODEL_PATH = "models/en_US-john-medium.onnx"
voice = None

print("[!] JARVIS Voice Model loading...")
try:
    voice = PiperVoice.load(MODEL_PATH)
    print("[+] Voice model ready!")
except Exception as e:
    print(f"[-] Model failed: {e}")

# Global PyAudio instance for cleaner management
p = pyaudio.PyAudio()

def jarvis_konus(metin):
    if not voice: return
    try:
        # Create a new stream for each speech to avoid conflicts
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=22050, output=True)
        
        # Synthesize and play directly to the stream
        for chunk in voice.synthesize(metin):
            stream.write(chunk.audio_int16_bytes)
        
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"[-] TTS Error: {e}")

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json(silent=True) or {}
    action = data.get('action')
    args = data.get('args', {})
    print(f"[x] Command: {action}")

    try:
        if action == "open_program":
            prog = args.get("name", "")
            if prog.lower().startswith("http"):
                webbrowser.open(prog)
            else:
                pyautogui.press("win")
                time.sleep(1)
                pyautogui.write(prog, interval=0.1)
                time.sleep(0.5)
                pyautogui.press("enter")
            return jsonify({"status": "success", "message": f"{prog} started."})

        elif action == "close_program":
            prog = args.get("name", "")
            # Alt+F4 ile aktif programı kapat
            pyautogui.hotkey("alt", "f4")
            return jsonify({"status": "success", "message": f"Closing {prog}."})

        elif action == "close_all_programs":
            # Tüm pencereleri kapat (Windows+D sonra Alt+F4)
            pyautogui.hotkey("win", "d")
            time.sleep(0.5)
            for _ in range(10):  # En fazla 10 pencere kapat
                pyautogui.hotkey("alt", "tab")
                time.sleep(0.2)
                pyautogui.hotkey("alt", "f4")
                time.sleep(0.3)
            return jsonify({"status": "success", "message": "Closing all programs."})

        elif action == "system_status":
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            return jsonify({"status": "success", "message": f"Diagnostics: CPU {cpu}%, RAM {ram}%. All systems nominal, Sir."})

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
                webbrowser.open("https://gemini.google.com")
                time.sleep(1)
                webbrowser.open("https://www.youtube.com/watch?v=XMEXPkPmmq0") 
                time.sleep(1)
                pyautogui.press("win")
                time.sleep(1)
                pyautogui.write("code")
                pyautogui.press("enter")
                return jsonify({"status": "success", "message": "Work protocols engaged."})

        elif action == "type_text":
            pyautogui.write(args.get("text", ""), interval=0.01)
            return jsonify({"status": "success"})

        return jsonify({"status": "success", "message": "Action completed."})
    except Exception as e:
        print(f"[-] Error: {e}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    metin = data.get('text', '')
    threading.Thread(target=jarvis_konus, args=(metin,), daemon=True).start()
    return jsonify({"status": "success"})

@app.route('/music/file')
def get_music():
    return send_from_directory('Sound', 'The Clash - Should I Stay or Should I Go (Official Audio) [BN1WwnEDWAM].mp3')

@app.route('/clap-status', methods=['GET'])
def clap_status():
    global clap_detected_flag
    status = clap_detected_flag
    clap_detected_flag = False # Reset after reading
    return jsonify({"detected": status})

@app.route('/music/control', methods=['POST'])
def music_control():
    data = request.get_json()
    action = data.get('action')
    
    try:
        if action == 'play':
            if mixer.music.get_busy():
                mixer.music.unpause()
            else:
                mixer.music.load("Sound/The Clash - Should I Stay or Should I Go (Official Audio) [BN1WwnEDWAM].mp3")
                mixer.music.set_volume(0.05)  # %5 ses seviyesi - çok düşük
                mixer.music.play()
            return jsonify({"status": "success", "message": "Playing"})
        
        elif action == 'pause':
            mixer.music.pause()
            return jsonify({"status": "success", "message": "Paused"})
        
        elif action == 'stop':
            mixer.music.stop()
            return jsonify({"status": "success", "message": "Stopped"})
        
        elif action == 'volume':
            volume = float(data.get('volume', 0.3))
            mixer.music.set_volume(volume)
            return jsonify({"status": "success", "message": f"Volume set to {int(volume*100)}%"})
        
        elif action == 'status':
            is_playing = mixer.music.get_busy()
            return jsonify({"status": "success", "playing": is_playing})
        
        return jsonify({"status": "error", "message": "Unknown action"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def alkis_dinle():
    CHUNK, RATE, THRESHOLD = 1024, 44100, 100  # Çok düşük threshold - test için
    p_in = pyaudio.PyAudio()
    
    # Mikrofon cihazlarını listele
    print("[DEBUG] Available audio devices:")
    for i in range(p_in.get_device_count()):
        info = p_in.get_device_info_by_index(i)
        if info['maxInputChannels'] > 0:
            print(f"  Device {i}: {info['name']} - {info['maxInputChannels']} channels")
    
    try:
        # Default mikrofonu kullan
        stream = p_in.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print("[*] Clap Sensor is Active...")
        
        frame_count = 0
        
        while True:
            try:
                data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
                volume = np.max(np.abs(data))
                
                # Debug: Her 50 frame'de bir ses seviyesini göster (daha sık)
                frame_count += 1
                if frame_count % 50 == 0:
                    print(f"[DEBUG] Audio level: {volume} (threshold: {THRESHOLD})")
                
                if volume > THRESHOLD:
                    print(f"[!] Clap detected! Volume: {volume}")
                    
                    global clap_detected_flag
                    clap_detected_flag = True
                    print("[+] Clap flagged for UI")
                    
                    # Şarkıyı başlat
                    try:
                        mixer.music.load("Sound/The Clash - Should I Stay or Should I Go (Official Audio) [BN1WwnEDWAM].mp3")
                        mixer.music.set_volume(0.05)
                        mixer.music.play()
                        print("[+] Music started playing")
                    except Exception as e:
                        print(f"[-] Music error: {e}")
                    
                    # Ses ile aynı anda
                    threading.Thread(target=jarvis_konus, args=("Good evening, Sir. All systems are online and ready for your command. Welcome back.",), daemon=True).start()
                    
                    stream.stop_stream()
                    stream.close()
                    print("[*] Clap Sensor Disabled after detection.")
                    return  # Fonksiyondan çık, bir daha dinleme
                    
            except Exception as e:
                print(f"[DEBUG] Audio read error: {e}")
                continue
                
    except Exception as e:
        print(f"[-] Microphone error: {e}")
        print("[!] Make sure microphone permissions are granted!")

if __name__ == '__main__':
    threading.Thread(target=alkis_dinle, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
