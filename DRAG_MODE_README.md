# 🖱️ Drag Mode - Pencere Sürükleme Özelliği

## 🎯 Özellik

Artık **baş parmak ve yüzük parmağını birleştirerek** aktif pencereyi **havada sürükleyebilirsin**!

## 🚀 Nasıl Çalışır?

### 1. Parmakları Birleştir
- **Baş parmak (THUMB)** + **Yüzük parmak (RING)** birleştir
- Mesafe < 50px olduğunda **DRAG MODE** aktif olur
- Yeşil "DRAGGING!" yazısı görünür

### 2. Elini Hareket Ettir
- Elini yukarı/aşağı/sağa/sola hareket ettir
- Mouse cursor elini takip eder
- Aktif pencere sürüklenir

### 3. Parmakları Ayır
- Parmakları ayır
- **DRAG MODE** kapanır
- Pencere bırakılır

## 🎮 Kullanım Senaryoları

### Pencere Taşıma
```
1. Taşımak istediğin pencereyi aktif et
2. Parmakları birleştir
3. Elini hareket ettir
4. Parmakları ayır
```

### Sürekli Sürükleme
```
1. Parmakları birleşik tut
2. Elini istediğin gibi hareket ettir
3. Pencere sürekli takip eder
```

### Hassas Kontrol
```
- Yavaş hareket = Hassas kontrol
- Hızlı hareket = Hızlı taşıma
- Smoothing aktif = Yumuşak geçişler
```

## 📊 Arayüz Bilgileri

### Bilgi Paneli
```
┌─────────────────────────────┐
│ HAND TRACKING DEBUG         │
│ Distance: 35.2px            │
│ Gesture: DRAG MODE          │
│ Hand Side: NONE             │
│ Drag Mode: ACTIVE           │ ← Yeni!
│ Thumb: (640, 320)           │
│ Ring: (660, 340)            │
└─────────────────────────────┘
```

### Ekran Göstergeleri
- **Yeşil Daire**: Trigger aktif
- **"DRAGGING!"**: Sürükleme modu
- **Cursor: (x, y)**: Mouse pozisyonu (sağ üst)

## ⚙️ Teknik Detaylar

### Koordinat Dönüşümü
```python
# El pozisyonu (0-1 normalized)
hand_x = wrist.x  # 0.0 - 1.0
hand_y = wrist.y  # 0.0 - 1.0

# Ekran koordinatları
screen_x = hand_x * screen_width
screen_y = hand_y * screen_height
```

### Smoothing
```python
smoothing_factor = 0.3  # 0.0 - 1.0
# 0.0 = Çok yumuşak (yavaş)
# 1.0 = Hiç smoothing (anlık)
```

### Mesafe Threshold
```python
if distance < 50:  # piksel
    drag_mode = True
```

## 🔧 Ayarlar

### Smoothing Değiştir
`hand_tracking_debug.py` dosyasında:
```python
smoothing_factor = 0.3  # Varsayılan
# 0.1 = Çok yumuşak
# 0.5 = Orta
# 0.8 = Hızlı
```

### Mesafe Hassasiyeti
```python
if distance < 50:  # Varsayılan
# 30 = Çok hassas (parmaklar çok yakın olmalı)
# 70 = Gevşek (parmaklar uzakta bile tetiklenir)
```

## 🐛 Sorun Giderme

### Mouse Çok Hızlı Hareket Ediyor
```python
smoothing_factor = 0.1  # Daha yumuşak yap
```

### Mouse Çok Yavaş
```python
smoothing_factor = 0.7  # Daha hızlı yap
```

### Yanlışlıkla Tetikleniyor
```python
if distance < 30:  # Daha hassas yap
```

### Pencere Sürüklenmiyor
- Pencereyi önce tıklayarak aktif et
- Bazı pencereler (sistem pencereleri) sürüklenemez
- Windows izinlerini kontrol et

## 💡 İpuçları

### En İyi Performans
1. **Işık**: İyi aydınlatılmış ortam
2. **Arka Plan**: Düz, tek renkli
3. **Mesafe**: Kameradan 30-50cm uzakta
4. **El Pozisyonu**: Avuç içi kameraya dönük

### Hassas Kontrol
- Elini yavaş hareket ettir
- Küçük hareketler yap
- Smoothing'i düşük tut

### Hızlı Hareket
- Smoothing'i yüksek tut
- Geniş hareketler yap
- Mesafe threshold'u artır

## 🎯 Kullanım Örnekleri

### Örnek 1: Tarayıcı Penceresi Taşıma
```
1. Chrome/Firefox'u aç
2. Hand tracking'i başlat
3. Parmakları birleştir
4. Tarayıcıyı istediğin yere taşı
5. Parmakları ayır
```

### Örnek 2: Çoklu Monitör
```
1. Pencereyi sol monitörde aç
2. Parmakları birleştir
3. Elini sağa hareket ettir
4. Pencere sağ monitöre geçer
```

### Örnek 3: Hassas Yerleştirme
```
1. Smoothing = 0.1 yap
2. Parmakları birleştir
3. Yavaş, küçük hareketler yap
4. Piksel hassasiyetinde yerleştir
```

## 🔐 Güvenlik

- **FAILSAFE kapalı**: Köşeye gittiğinde durmuyor
- **Sadece aktif pencere**: Diğer pencereler etkilenmez
- **Lokal işlem**: İnternet bağlantısı gerektirmez

## 📝 Notlar

- PyAutoGUI kullanılıyor
- Windows, macOS, Linux destekli
- Gerçek zamanlı koordinat dönüşümü
- Yumuşak geçişler için smoothing

---

**Coded by Semih Ergili** 🚀
