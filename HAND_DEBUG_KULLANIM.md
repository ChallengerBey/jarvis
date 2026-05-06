# 🖐️ Hand Tracking Debug Tool - Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### Kurulum ve Çalıştırma

1. **Otomatik Kurulum** (Önerilen):
   ```bash
   run_hand_debug.bat
   ```

2. **Manuel Kurulum**:
   ```bash
   pip install -r requirements_hand.txt
   python hand_tracking_debug.py
   ```

## 📹 Kamera Seçimi

Program başladığında otomatik olarak tüm kameraları tarar:

```
🔍 Kameralar aranıyor...

   ✅ Kamera 0 bulundu (DirectShow) - 640x480
   ✅ Kamera 1 bulundu (DirectShow) - 1280x720

==================================================
KAMERA SEÇİMİ
==================================================
   [1] Kamera 0 - DirectShow (640x480)
   [2] Kamera 1 - DirectShow (1280x720)
==================================================

Kamera seçin (1-2): 
```

**Özellikler:**
- ✅ Otomatik kamera tarama (0-4 arası)
- ✅ Birden fazla backend desteği (DirectShow, Media Foundation)
- ✅ Çözünürlük bilgisi
- ✅ Kolay seçim menüsü

## 📊 Arayüz Özellikleri

### Görsel Elemanlar

- **🔴 Kırmızı Noktalar**: El iskelet noktaları (21 nokta)
- **⚪ Beyaz Çizgiler**: Parmak bağlantıları
- **🔵 Cyan Daire (THUMB)**: Baş parmak ucu
- **🟣 Magenta Daire (RING)**: Yüzük parmak ucu
- **📏 Bağlantı Çizgisi**: İki parmak arası mesafe
  - Beyaz: Normal (>50px)
  - Yeşil: Tetiklendi (<50px)

### Bilgi Paneli (Sol Üst)

```
┌─────────────────────────────┐
│ HAND TRACKING DEBUG         │
│ Distance: 45.2px            │
│ Gesture: NEXT TAB           │
│ Hand Side: RIGHT            │
│ Thumb: (640, 320)           │
│ Ring: (680, 340)            │
└─────────────────────────────┘
```

### Ekran Bölgeleri

- **Sol Taraf**: PREV TAB (önceki sekme)
- **Orta Çizgi**: Ekran bölme çizgisi
- **Sağ Taraf**: NEXT TAB (sonraki sekme)

## 🎮 Nasıl Kullanılır?

1. **Programı Başlat**: `run_hand_debug.bat` çalıştır
2. **Elini Kameraya Göster**: Tek el yeterli
3. **Baş Parmak + Yüzük Parmak Birleştir**:
   - Mesafe < 50px olduğunda tetiklenir
   - Yeşil "TRIGGERED!" yazısı görünür
   - Yeşil ok yönü gösterir

### Gesture Tespiti

| El Pozisyonu | Mesafe | Sonuç |
|-------------|--------|-------|
| Sağ tarafta | <50px  | ➡️ NEXT TAB |
| Sol tarafta | <50px  | ⬅️ PREV TAB |
| Herhangi    | >50px  | ❌ NONE |

## 🔧 Ayarlar

### Hassasiyet Ayarı

`hand_tracking_debug.py` dosyasında:

```python
# Mesafe eşiği (varsayılan: 50)
if distance < 50:  # Bu değeri değiştir
    gesture = "TRIGGERED"
```

### Kamera Çözünürlüğü

```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)   # Genişlik
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)   # Yükseklik
```

## 🐛 Sorun Giderme

### Kamera Açılmıyor
```bash
# Kamera index'ini değiştir
cap = cv2.VideoCapture(1)  # 0 yerine 1 dene
```

### Paket Kurulum Hatası
```bash
# Python ve pip güncellemesi
python -m pip install --upgrade pip
pip install opencv-python mediapipe
```

### El Algılanmıyor
- Işık yeterli mi kontrol et
- Eli kameraya daha yakın tut
- Arka plan karmaşık olmasın

## ⌨️ Kısayollar

- **ESC**: Programdan çık
- **Kamera**: Otomatik aynalama aktif

## 📝 Teknik Detaylar

- **Framework**: MediaPipe Hands
- **Parmak Noktaları**: 
  - Thumb tip: Landmark 4
  - Ring finger tip: Landmark 16
  - Wrist center: Landmark 9
- **Mesafe Hesaplama**: Euclidean distance
- **FPS**: ~30 FPS (kameraya bağlı)

## 🎯 Developer Notları

Bu tool, web arayüzündeki hand tracking'in doğru çalışıp çalışmadığını test etmek için tasarlandı.

### Web Entegrasyonu İçin

1. Mesafe threshold'u aynı tut (50px)
2. Landmark indexleri aynı (4, 16, 9)
3. Ekran bölme mantığı aynı (center line)

---

**Coded by Semih Ergili** 🚀
