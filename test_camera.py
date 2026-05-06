"""
Kamera Test Scripti
Kameranın düzgün çalışıp çalışmadığını test eder
"""
import cv2
import sys

print("=" * 50)
print("KAMERA TEST ARACI")
print("=" * 50)
print()

# Farklı backend'leri dene
backends = [
    (cv2.CAP_DSHOW, "DirectShow (Windows)"),
    (cv2.CAP_MSMF, "Media Foundation (Windows)"),
    (cv2.CAP_ANY, "Otomatik")
]

camera_found = False
working_backend = None
working_index = None

print("🔍 Kamera aranıyor...\n")

# Kamera index'lerini dene (0-2)
for cam_index in range(3):
    for backend, backend_name in backends:
        try:
            print(f"   Deneniyor: Kamera {cam_index} - {backend_name}...", end=" ")
            cap = cv2.VideoCapture(cam_index, backend)
            
            if cap.isOpened():
                ret, frame = cap.read()
                if ret and frame is not None:
                    print("✅ BAŞARILI!")
                    camera_found = True
                    working_backend = (backend, backend_name)
                    working_index = cam_index
                    cap.release()
                    break
                else:
                    print("❌ Frame okunamadı")
                    cap.release()
            else:
                print("❌ Açılamadı")
        except Exception as e:
            print(f"❌ Hata: {e}")
    
    if camera_found:
        break

print()
print("=" * 50)

if camera_found:
    print("✅ KAMERA BULUNDU!")
    print(f"   Index: {working_index}")
    print(f"   Backend: {working_backend[1]}")
    print()
    
    # Kamerayı aç ve göster
    print("🎥 Kamera önizlemesi açılıyor... (ESC ile çık)")
    print()
    cap = cv2.VideoCapture(working_index, working_backend[0])
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        frame = cv2.flip(frame, 1)
        
        # Bilgi yaz
        cv2.putText(frame, "KAMERA CALISIYOR!", (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Index: {working_index} | Backend: {working_backend[1]}", 
                   (50, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(frame, "ESC ile cik", (50, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        cv2.imshow('Kamera Test', frame)
        
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
else:
    print("❌ KAMERA BULUNAMADI!")
    print()
    print("🔧 Çözüm Önerileri:")
    print("   1. Başka bir uygulama kamerayı kullanıyor olabilir")
    print("      (Zoom, Teams, Skype, vb. kapatın)")
    print()
    print("   2. Windows Ayarlar > Gizlilik > Kamera")
    print("      - 'Uygulamaların kamerama erişmesine izin ver' AÇIK olmalı")
    print("      - Python için izin verilmiş olmalı")
    print()
    print("   3. Kamera sürücülerini kontrol edin")
    print("      - Aygıt Yöneticisi > Kameralar")
    print()
    print("   4. Harici kamera kullanıyorsanız USB bağlantısını kontrol edin")
    print()

print("=" * 50)
input("\nÇıkmak için Enter'a basın...")
