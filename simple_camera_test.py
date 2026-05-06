"""
Basit Kamera Test - Sadece görüntü göster
"""
import cv2

print("=" * 50)
print("BASİT KAMERA TESTİ")
print("=" * 50)
print()

# Kamera 0'ı DirectShow ile aç
print("Kamera açılıyor...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Kamera 0 açılamadı, kamera 1 deneniyor...")
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("❌ Hiç kamera açılamadı!")
    input("Enter'a basın...")
    exit(1)

print("✅ Kamera açıldı!")
print("ESC ile çıkış yapın")
print()

frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print(f"Frame {frame_count}: ❌ Okunamadı")
        continue
    
    if frame is None:
        print(f"Frame {frame_count}: ❌ None")
        continue
    
    frame_count += 1
    
    # Aynala
    frame = cv2.flip(frame, 1)
    
    # Bilgi yaz
    cv2.putText(frame, f"Frame: {frame_count}", (20, 40), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "ESC = Exit", (20, 80), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Göster
    cv2.imshow('Simple Camera Test', frame)
    
    # ESC ile çık - waitKey artırıldı
    key = cv2.waitKey(30) & 0xFF
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
print(f"\n✅ Test tamamlandı. Toplam {frame_count} frame gösterildi.")
input("Enter'a basın...")
