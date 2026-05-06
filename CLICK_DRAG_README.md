# 🖱️ Click & Drag - Gelişmiş Mouse Kontrolü

## 🎯 Yeni Özellikler

Artık **iki farklı parmak kombinasyonu** ile tam mouse kontrolü!

### 1️⃣ Baş Parmak + İşaret Parmağı
- **Bir kere birleştir** → Sol Click (mouseDown)
- **Basılı tut** → Sürükle (Drag)
- **Parmakları ayır** → Bırak (mouseUp)

### 2️⃣ Baş Parmak + Yüzük Parmağı
- **Birleştir** → Mouse hareket ettir
- **Elini hareket ettir** → Cursor takip eder
- **Parmakları ayır** → Hareket durdur

## 🎮 Kullanım Senaryoları

### Dosya Sürükleme
```
1. Dosyanın üzerine git (Baş+Yüzük ile mouse hareket)
2. Baş+İşaret birleştir (Click)
3. Basılı tut
4. Elini hareket ettir (Dosya sürüklenir)
5. Parmakları ayır (Dosya bırakılır)
```

### Metin Seçme
```
1. Metnin başına git
2. Baş+İşaret birleştir
3. Basılı tutarak elini hareket ettir
4. Metin seçilir
5. Parmakları ayır
```

### Buton Tıklama
```
1. Butonun üzerine git (Baş+Yüzük)
2. Baş+İşaret bir kere birleştir-ayır
3. Click yapıldı!
```

### Pencere Taşıma
```
1. Pencere başlığına git
2. Baş+İşaret birleştir
3. Basılı tut
4. Elini hareket ettir
5. Pencere taşınır
```

## 📊 Görsel Feedback

### Baş Parmak + İşaret Parmağı
- **Yeşil çizgi**: Parmaklar birleşik
- **"CLICKING!"**: İlk temas
- **"DRAGGING!"**: Sürükleme modu
- **Yeşil daire**: Aktif trigger

### Baş Parmak + Yüzük Parmağı
- **Magenta çizgi**: Parmaklar birleşik
- **"MOVING!"**: Mouse hareket modu
- **Magenta daire**: Aktif trigger
- **Cursor pozisyonu**: Sağ üstte

## 🎨 Parmak Renkleri

- **Baş Parmak (THUMB)**: Cyan (Mavi-Yeşil)
- **İşaret Parmağı (INDEX)**: Yeşil
- **Yüzük Parmağı (RING)**: Magenta (Pembe)

## 📋 Bilgi Paneli

```
┌─────────────────────────────────┐
│ HAND TRACKING DEBUG             │
│ Thumb-Index: 35.2px             │ ← Click/Drag mesafesi
│ Thumb-Ring: 120.5px             │ ← Mouse move mesafesi
│ Gesture: DRAGGING               │
│ Hand Side: NONE                 │
│ Click Mode: ACTIVE              │ ← Sol click basılı
│ Drag Mode: OFF                  │ ← Mouse move modu
│ Thumb: (640, 320)               │
│ Index: (680, 340)               │
└─────────────────────────────────┘
```

## ⚙️ Teknik Detaylar

### Mesafe Threshold
```python
if distance_index < 50:  # Baş+İşaret
    # Click/Drag
    
if distance_ring < 50:   # Baş+Yüzük
    # Mouse move
```

### Click Mantığı
```python
# İlk temas
pyautogui.mouseDown()  # Sol click bas

# Basılı tutma
pyautogui.moveTo(x, y)  # Sürükle

# Bırakma
pyautogui.mouseUp()  # Sol click bırak
```

### Smoothing
```python
smoothing_factor = 0.3  # 0.0 - 1.0
# Yumuşak mouse hareketi için
```

## 🔧 Ayarlar

### Mesafe Hassasiyeti
`hand_tracking_debug.py` dosyasında:
```python
if distance_index < 50:  # Click/Drag threshold
if distance_ring < 50:   # Mouse move threshold
```

### Smoothing Hızı
```python
smoothing_factor = 0.3  # Varsayılan
# 0.1 = Çok yumuşak
# 0.5 = Orta
# 0.8 = Hızlı
```

## 🐛 Sorun Giderme

### Click Yapılmıyor
- Parmakları daha yakın getir
- Mesafe < 50px olmalı
- Yeşil çizgi görünmeli

### Sürükleme Çalışmıyor
- Parmakları birleşik tut
- "DRAGGING!" yazısı görünmeli
- Elini yavaşça hareket ettir

### Mouse Çok Hızlı
```python
smoothing_factor = 0.1  # Daha yumuşak
```

### Yanlışlıkla Click Oluyor
```python
if distance_index < 30:  # Daha hassas
```

## 💡 İpuçları

### Hassas Kontrol
1. Smoothing'i düşük tut (0.1-0.2)
2. Yavaş hareketler yap
3. Parmakları sabit tut

### Hızlı Kullanım
1. Smoothing'i yükselt (0.5-0.7)
2. Geniş hareketler yap
3. Threshold'u artır (60-70px)

### En İyi Performans
- İyi ışık
- Düz arka plan
- Kameradan 30-50cm uzakta
- Avuç içi kameraya dönük

## 🎯 Pratik Örnekler

### Örnek 1: Dosya Kopyalama
```
1. Dosyaya git (Baş+Yüzük)
2. Baş+İşaret birleştir
3. Ctrl tuşuna bas (klavyeden)
4. Sürükle (Baş+İşaret basılı)
5. Bırak
```

### Örnek 2: Çoklu Seçim
```
1. İlk öğeye tıkla (Baş+İşaret)
2. Shift tuşuna bas (klavyeden)
3. Son öğeye tıkla
4. Çoklu seçim yapıldı
```

### Örnek 3: Sağ Click (Gelecek)
```
Şu an sadece sol click destekleniyor
Sağ click için: Baş+Orta parmak (yakında)
```

## 🔐 Güvenlik

- **Lokal işlem**: İnternet gerektirmez
- **Sadece mouse kontrolü**: Klavye etkilenmez
- **Otomatik bırakma**: El algılanmazsa click bırakılır

## 📝 Notlar

- PyAutoGUI kullanılıyor
- Gerçek zamanlı mouse kontrolü
- Yumuşak geçişler (smoothing)
- Çift parmak kombinasyonu

---

**Coded by Semih Ergili** 🚀
