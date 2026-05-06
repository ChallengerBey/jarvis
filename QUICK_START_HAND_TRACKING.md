# 🚀 Hand Tracking - Hızlı Başlangıç

## 🎯 Yeni Özellik: DRAG MODE! 🖱️

Artık **parmak hareketleriyle pencere sürükleyebilirsin**!

## 🖐️ Nasıl Kullanılır?

### Drag Mode (Pencere Sürükleme)

1. **Parmakları Birleştir**: Baş parmak + Yüzük parmak
2. **Elini Hareket Ettir**: Mouse cursor elini takip eder
3. **Parmakları Ayır**: Pencere bırakılır

```
Parmaklar Birleşik = DRAG MODE ACTIVE
Elini Hareket Ettir = Pencere Sürüklenir
Parmakları Ayır = Pencere Bırakılır
```

## 🎯 İki Farklı Test Yöntemi

### 1️⃣ Python Debug Tool (Önerilen - Developer için)

**En iyi görselleştirme ve debug için!**

```bash
# Çalıştır
run_hand_debug.bat

# veya manuel
pip install -r requirements_hand.txt
python hand_tracking_debug.py
```

**Özellikler:**
- ✅ Tam el iskeleti görünümü (21 nokta)
- ✅ Gerçek zamanlı mesafe göstergesi
- ✅ Gesture tetikleme feedback'i
- ✅ Sol/Sağ bölge göstergesi
- ✅ Bilgi paneli (distance, gesture, hand side)
- ✅ Yüksek çözünürlük (1280x720)

### 2️⃣ Web Arayüzü (Production)

```bash
cd "Kaynak Kod"
npm run dev
```

**Özellikler:**
- ✅ JARVIS 3D görselleştirme
- ✅ Küçük debug preview (sağ alt)
- ✅ Sekme navigasyonu
- ✅ Sistem logları
- ✅ Tam entegrasyon

## 🖐️ Nasıl Kullanılır?

### Gesture: Baş Parmak + Yüzük Parmak

1. **Elini kameraya göster** (tek el yeterli)
2. **Baş parmak ve yüzük parmağını birleştir**
3. **Mesafe < 30-50px olduğunda tetiklenir**

### Yön Kontrolü

```
┌─────────────┬─────────────┐
│             │             │
│    LEFT     │    RIGHT    │
│             │             │
│  ⬅️ PREV    │   NEXT ➡️   │
│             │             │
└─────────────┴─────────────┘
```

- **Sol tarafta birleştir** → Önceki sekme
- **Sağ tarafta birleştir** → Sonraki sekme

## 📊 Karşılaştırma

| Özellik | Python Tool | Web Arayüzü |
|---------|-------------|-------------|
| Görselleştirme | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Debug Bilgisi | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Kullanım Kolaylığı | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Entegrasyon | ❌ | ✅ |
| Performans | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🔧 Sorun Giderme

### Python Tool Çalışmıyor
```bash
# OpenCV ve MediaPipe yeniden kur
pip uninstall opencv-python mediapipe
pip install opencv-python==4.8.1.78 mediapipe==0.10.8
```

### Web Arayüzü Çalışmıyor
```bash
# Node modüllerini temizle
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Kamera Açılmıyor
- Başka uygulama kamerayı kullanıyor olabilir
- Kamera izinlerini kontrol et
- Farklı kamera index'i dene (Python: `cv2.VideoCapture(1)`)

## 📝 Notlar

- **Python tool** geliştirme ve test için idealdir
- **Web arayüzü** son kullanıcı için tasarlanmıştır
- Her iki yöntem de aynı algoritmaları kullanır
- Mesafe threshold'ları senkronize tutulmuştur

## 🎮 Kısayollar

### Python Tool
- **ESC**: Çıkış

### Web Arayüzü
- **El İkonu**: Hand tracking aç/kapat
- **Settings İkonu**: Ayarlar paneli

---

**Coded by Semih Ergili** 🚀
