import cv2
import sys

print("ULTRA SIMPLE CAMERA TEST")
print("=" * 50)

# Kamera 0'ı aç
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("HATA: Kamera açılamadı!")
    input()
    sys.exit(1)

print("Kamera açıldı!")
print("Frame okuma testi...")

# 10 frame dene
for i in range(10):
    ret, frame = cap.read()
    print(f"Frame {i}: ret={ret}, frame={'OK' if frame is not None else 'NONE'}")
    
    if ret and frame is not None:
        print(f"  Frame shape: {frame.shape}")
        print(f"  Frame dtype: {frame.dtype}")
        print(f"  Frame min/max: {frame.min()}/{frame.max()}")
        
        # Pencere oluştur
        cv2.namedWindow('Test', cv2.WINDOW_NORMAL)
        cv2.imshow('Test', frame)
        
        print("Pencere gösterildi! 3 saniye bekle...")
        key = cv2.waitKey(3000)
        print(f"WaitKey sonucu: {key}")
        
        if key == 27:
            break
        
        break  # İlk başarılı frame'de dur

cap.release()
cv2.destroyAllWindows()

print("\nTest tamamlandı!")
input("Enter'a bas...")
