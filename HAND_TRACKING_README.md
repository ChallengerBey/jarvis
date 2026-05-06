# 🖐️ Parmak Takibi ile Sekme Kontrolü

## Nasıl Çalışır?

JARVIS arayüzüne **parmak takibi** özelliği eklendi! Artık kameradan baş parmak ve yüzük parmağınızı birleştirerek sekmeleri kontrol edebilirsiniz.

## Kullanım

1. **Hand Tracking Butonuna Tıklayın**: Sağ üst köşede el ikonu bulunan butona tıklayın
2. **Kamera İzni Verin**: Tarayıcı kamera erişimi isteyecek, izin verin
3. **Parmak Hareketleri**:
   - **Baş parmak + Yüzük parmak** birleştirin
   - **Sağ tarafta** birleştirirseniz → Sonraki sekme
   - **Sol tarafta** birleştirirseniz → Önceki sekme

## Sekmeler

- Home
- Music
- Settings
- Logs
- System

## Teknik Detaylar

- **TensorFlow.js** ve **Hand Pose Detection** kullanılıyor
- Gerçek zamanlı parmak takibi
- 500ms cooldown ile yanlışlıkla çoklu tetikleme önleniyor
- Mesafe < 30 piksel olduğunda tetikleniyor

## Özellikler

✅ Gerçek zamanlı el takibi
✅ Baş parmak ve yüzük parmak tespiti
✅ Sağ/Sol yön algılama
✅ Sekme geçişi animasyonları
✅ Sistem loglarında bildirim

---

**Coded by Semih Ergili** 🚀
