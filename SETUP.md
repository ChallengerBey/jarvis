# 🚀 J.A.R.V.I.S + Hand Tracking - Kurulum Rehberi

## 📋 Sistem Gereksinimleri

- **İşletim Sistemi**: Windows 10/11
- **Python**: 3.8 veya üzeri
- **Node.js**: 18.0 veya üzeri
- **Kamera**: Webcam veya harici USB kamera
- **RAM**: Minimum 4GB (8GB önerilen)
- **İnternet**: İlk kurulum için gerekli

---

## 🔧 Kurulum Adımları

### 1️⃣ Python Kurulumu

**Kontrol:**
```bash
python --version
```

**Kurulum (eğer yoksa):**
- `Python(PATCH)/python-manager-26.1.msix` dosyasını çalıştır
- Veya https://www.python.org/downloads/ adresinden indir

**Önemli:** Kurulum sırasında "Add Python to PATH" seçeneğini işaretle!

---

### 2️⃣ Node.js Kurulumu

**Kontrol:**
```bash
node --version
npm --version
```

**Kurulum (eğer yoksa):**
- `Node.js/node-v24.15.0-x64.msi` dosyasını çalıştır
- Veya https://nodejs.org/en/download/ adresinden indir

---

### 3️⃣ Python Paketlerini Kur

**Otomatik Kurulum (Önerilen):**
```bash
cd "Kaynak Kod"
python install_deps.py
```

Bu script şunları kurar:
- ✅ Flask ve Flask-CORS (JARVIS server)
- ✅ PyAutoGUI (mouse/keyboard kontrolü)
- ✅ OpenCV (kamera işleme)
- ✅ MediaPipe (el takibi)
- ✅ Diğer JARVIS bağımlılıkları

**Manuel Kurulum:**
```bash
pip install -r requirements_hand.txt
```

---

### 4️⃣ Node.js Paketlerini Kur

```bash
cd "Kaynak Kod"
npm install
```

**Eğer hata alırsan:**
```bash
# Önce temizle
rm -rf node_modules package-lock.json

# Sonra tekrar kur
npm install
```

---

### 5️⃣ Kamera İzinlerini Ayarla

**Windows Ayarları:**
1. Başlat → Ayarlar → Gizlilik ve güvenlik
2. Kamera
3. "Uygulamaların kamerama erişmesine izin ver" → **AÇIK**
4. Python ve tarayıcı için izin ver

**Test:**
```bash
python test_camera.py
```

Kamera görüntüsü geliyorsa ✅

---

## 🎮 Çalıştırma

### Hand Tracking Debug Tool
```bash
python hand_tracking_debug.py
```

**Özellikler:**
- 🖐️ Gerçek zamanlı el takibi
- 🖱️ Mouse kontrolü (Baş+İşaret = Click, Baş+Yüzük = Move)
- 📊 Debug bilgileri
- 🎥 Kamera seçimi

### JARVIS Flask Server
```bash
python jarvis_app.py
```

**Port:** http://localhost:8080

### Web Arayüzü (Next.js)
```bash
npm run dev
```

**URL:** http://localhost:3000

---

## 🐛 Sorun Giderme

### Kamera Açılmıyor

**Sorun:** "Kamera bulunamadı" hatası

**Çözüm:**
1. Başka uygulama kamerayı kullanıyor olabilir (Zoom, Teams, Skype)
2. Kamera izinlerini kontrol et
3. USB kamerayı çıkar-tak
4. `test_camera.py` ile test et

### OpenCV Kurulumu Başarısız

**Sorun:** `pip install opencv-python` hata veriyor

**Çözüm:**
```bash
# Önce pip'i güncelle
python -m pip install --upgrade pip

# Sonra tekrar dene
pip install opencv-python==4.8.1.78
```

### MediaPipe Kurulumu Başarısız

**Sorun:** `pip install mediapipe` hata veriyor

**Çözüm:**
```bash
# Python 3.8-3.11 arası olmalı
python --version

# Eğer 3.12+ ise, 3.11 kur
```

### PyAudio Kurulumu Başarısız

**Sorun:** "Microsoft Visual C++ 14.0 is required"

**Çözüm:**
1. https://visualstudio.microsoft.com/downloads/
2. "Build Tools for Visual Studio" indir
3. "C++ build tools" seçeneğini işaretle
4. Kur ve tekrar dene

**Alternatif:**
- PyAudio .whl dosyasını indir: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- `pip install PyAudio‑0.2.11‑cp311‑cp311‑win_amd64.whl`

### npm install Hatası

**Sorun:** "EACCES" veya "permission denied"

**Çözüm:**
```bash
# Node.js'i yönetici olarak çalıştır
# Veya:
npm cache clean --force
npm install
```

### Port Kullanımda

**Sorun:** "Port 8080 already in use"

**Çözüm:**
```bash
# Başka port kullan
# flask_server.py içinde:
app.run(port=8081)

# page.tsx içinde:
const [flaskUrl, setFlaskUrl] = useState("http://localhost:8081");
```

---

## 📝 Groq API Key

**JARVIS AI özellikleri için gerekli!**

1. https://console.groq.com/ adresine git
2. Hesap oluştur (ücretsiz)
3. API Key al
4. `page.tsx` içinde değiştir:

```javascript
const [groqKey, setGroqKey] = useState("BURAYA_KENDI_KEY_INI_YAZ");
```

---

## 🎯 Özellikler

### Hand Tracking
- ✅ Baş parmak + İşaret parmağı = Sol Click + Drag
- ✅ Baş parmak + Yüzük parmağı = Mouse Move + Tab Switch
- ✅ Gerçek zamanlı görsel feedback
- ✅ Kamera seçimi
- ✅ Hassasiyet ayarları

### JARVIS
- ✅ Ses tanıma ("Hey Jarvis")
- ✅ AI komut işleme (Groq)
- ✅ Sistem kontrolü
- ✅ Müzik kontrolü
- ✅ Alkış algılama

### Web Arayüzü
- ✅ 3D görselleştirme
- ✅ Hand tracking entegrasyonu
- ✅ Sekme sistemi
- ✅ Sistem logları
- ✅ Müzik kontrolü

---

## 📂 Proje Yapısı

```
Kaynak Kod/
├── app/                    # Next.js web arayüzü
│   ├── page.tsx           # Ana sayfa (hand tracking)
│   ├── layout.tsx         # Layout
│   └── globals.css        # Stiller
├── models/                # TTS modelleri (ZORUNLU!)
│   ├── en_GB-dany-medium.onnx
│   ├── en_US-danny-low.onnx
│   ├── en_US-john-medium.onnx
│   └── tr_model.onnx
├── public/                # Ses dosyaları
├── flask_server.py        # JARVIS backend
├── jarvis_app.py          # JARVIS ana uygulama
├── hand_tracking_debug.py # Hand tracking debug tool
├── test_camera.py         # Kamera test
├── install_deps.py        # Otomatik kurulum
├── requirements_hand.txt  # Python bağımlılıkları
├── package.json           # Node.js bağımlılıkları
└── SETUP.md              # Bu dosya
```

**⚠️ ÖNEMLİ:** `models/` klasörünü başka PC'ye kopyalamayı unutma! Yoksa JARVIS konuşamaz.

---

## 🚀 Hızlı Başlangıç (TL;DR)

```bash
# 1. Python paketleri
python install_deps.py

# 2. Node.js paketleri
npm install

# 3. Kamera test
python test_camera.py

# 4. Hand tracking
python hand_tracking_debug.py

# 5. Web arayüzü
npm run dev
```

---

## 💡 İpuçları

### En İyi Performans
- İyi aydınlatılmış ortam
- Düz, tek renkli arka plan
- Kameradan 30-50cm uzakta
- Avuç içi kameraya dönük

### Hassasiyet Ayarı
`hand_tracking_debug.py` içinde:
```python
if distance_index < 60:  # Daha hassas: 40, Daha gevşek: 80
```

### Smoothing Ayarı
```python
smoothing_factor = 0.3  # Daha yumuşak: 0.1, Daha hızlı: 0.7
```

---

## 📞 Destek

Sorun yaşıyorsan:
1. `test_camera.py` ile kamerayı test et
2. Console loglarını kontrol et (F12)
3. Python hatalarını oku
4. README dosyalarını oku

---

**Coded by Semih Ergili** 🚀
