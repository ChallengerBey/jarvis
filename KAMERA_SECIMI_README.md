# 📹 Kamera Seçimi Özelliği

## 🎯 Özellikler

Hand tracking debug tool artık **otomatik kamera tarama** ve **seçim menüsü** ile geliyor!

## 🚀 Nasıl Çalışır?

### 1. Otomatik Tarama

Program başladığında:
- 0-4 arası tüm kamera index'lerini tarar
- DirectShow ve Media Foundation backend'lerini dener
- Çalışan kameraları listeler

### 2. Kullanıcı Seçimi

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

Kamera seçin (1-2): 2

✅ Seçilen kamera: Kamera 1 (DirectShow)
✅ Kamera başarıyla başlatıldı! (1280x720)
```

### 3. Hand Tracking Başlar

Seçilen kamera ile hand tracking otomatik başlar.

## 🔧 Kullanım Senaryoları

### Laptop + Harici Kamera
```
[1] Kamera 0 - DirectShow (640x480)    ← Laptop kamerası
[2] Kamera 1 - DirectShow (1920x1080) ← Harici HD kamera
```
→ Daha iyi kalite için [2] seçin

### Birden Fazla USB Kamera
```
[1] Kamera 0 - DirectShow (640x480)
[2] Kamera 1 - DirectShow (1280x720)
[3] Kamera 2 - DirectShow (1920x1080)
```
→ İstediğiniz kamerayı seçin

### Tek Kamera
```
[1] Kamera 0 - DirectShow (640x480)
```
→ Otomatik olarak [1] seçin

## 🛠️ Test Araçları

### Kamera Test
```bash
test_camera.bat
```
- Tüm kameraları tarar
- İlk bulunan kamerayı açar
- Canlı önizleme gösterir

### Hand Tracking Debug
```bash
run_hand_debug.bat
```
- Kamera seçim menüsü
- Hand tracking ile test
- Tam debug arayüzü

## ❌ Sorun Giderme

### Hiç Kamera Bulunamadı

```
❌ Hiç kamera bulunamadı!

🔧 Çözüm Önerileri:
   1. Başka bir uygulama kamerayı kullanıyor olabilir (Zoom, Teams, Skype)
   2. Windows Ayarlar > Gizlilik > Kamera izinlerini kontrol edin
   3. Kamera USB bağlantısını kontrol edin
```

**Çözümler:**
1. Zoom, Teams, Skype gibi uygulamaları kapatın
2. Windows Ayarlar → Gizlilik → Kamera → İzinleri kontrol edin
3. USB kablosunu çıkarıp tekrar takın
4. Aygıt Yöneticisi'nden kamera sürücülerini kontrol edin

### Kamera Açıldı Ama Frame Gelmiyor

```
❌ Kamera açıldı ama frame okunamıyor!
```

**Çözümler:**
1. Farklı bir kamera seçin
2. Kamera sürücülerini güncelleyin
3. Bilgisayarı yeniden başlatın

### Düşük Çözünürlük

```
[1] Kamera 0 - DirectShow (640x480)  ← Düşük
```

**Çözümler:**
1. Harici HD kamera kullanın
2. Kamera ayarlarından çözünürlüğü artırın
3. Farklı backend deneyin (Media Foundation)

## 💡 İpuçları

### En İyi Performans
- 1280x720 veya üzeri çözünürlük seçin
- DirectShow backend genellikle daha hızlıdır
- Harici kamera laptop kamerasından daha iyidir

### Çoklu Kamera Kullanımı
- Her seferinde farklı kamera seçebilirsiniz
- Program her başlatıldığında yeniden tarama yapar
- Kamera ekleyip çıkarabilirsiniz

### Debug İçin
- `test_camera.bat` ile önce kamerayı test edin
- Çalışan kamera index'ini not edin
- Hand tracking'de aynı kamerayı seçin

## 🎮 Kısayollar

- **1-9**: Kamera seçimi
- **Enter**: Seçimi onayla
- **Ctrl+C**: Programdan çık
- **ESC**: Hand tracking penceresini kapat

## 📝 Teknik Detaylar

### Desteklenen Backend'ler
- **DirectShow (CAP_DSHOW)**: Windows native, hızlı
- **Media Foundation (CAP_MSMF)**: Modern Windows API

### Tarama Aralığı
- Index: 0-4 (5 kamera)
- Genişletilebilir (kod içinde değiştirilebilir)

### Çözünürlük Ayarı
- Varsayılan: 1280x720
- Otomatik fallback: Kameranın desteklediği maksimum

---

**Coded by Semih Ergili** 🚀
