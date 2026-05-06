import cv2
import mediapipe as mp
import math
import pyautogui
import time

# PyAutoGUI ayarları
pyautogui.FAILSAFE = False  # Köşeye gittiğinde durmasın
pyautogui.PAUSE = 0  # Hızlı hareket için delay yok

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def find_available_cameras():
    """Kullanılabilir kameraları bul"""
    available_cameras = []
    backends = [
        (cv2.CAP_DSHOW, "DirectShow"),
        (cv2.CAP_MSMF, "Media Foundation"),
    ]
    
    print("🔍 Kameralar aranıyor...\n")
    
    for cam_index in range(5):  # 0-4 arası kamera index'lerini dene
        for backend, backend_name in backends:
            try:
                cap = cv2.VideoCapture(cam_index, backend)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        # Kamera bilgilerini al
                        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        available_cameras.append({
                            'index': cam_index,
                            'backend': backend,
                            'backend_name': backend_name,
                            'resolution': f"{width}x{height}"
                        })
                        print(f"   ✅ Kamera {cam_index} bulundu ({backend_name}) - {width}x{height}")
                        cap.release()
                        break  # Bu index için başarılı, diğer backend'leri deneme
                cap.release()
            except:
                pass
    
    return available_cameras

def select_camera(cameras):
    """Kullanıcıdan kamera seçmesini iste"""
    if len(cameras) == 0:
        print("\n❌ Hiç kamera bulunamadı!")
        print("\n🔧 Çözüm Önerileri:")
        print("   1. Başka bir uygulama kamerayı kullanıyor olabilir (Zoom, Teams, Skype)")
        print("   2. Windows Ayarlar > Gizlilik > Kamera izinlerini kontrol edin")
        print("   3. Kamera USB bağlantısını kontrol edin")
        input("\nÇıkmak için Enter'a basın...")
        exit(1)
    
    print("\n" + "=" * 50)
    print("KAMERA SEÇİMİ")
    print("=" * 50)
    
    for i, cam in enumerate(cameras):
        print(f"   [{i+1}] Kamera {cam['index']} - {cam['backend_name']} ({cam['resolution']})")
    
    print("=" * 50)
    
    while True:
        try:
            choice = input(f"\nKamera seçin (1-{len(cameras)}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(cameras):
                return cameras[choice_idx]
            else:
                print(f"❌ Geçersiz seçim! 1-{len(cameras)} arası bir sayı girin.")
        except ValueError:
            print("❌ Lütfen bir sayı girin!")
        except KeyboardInterrupt:
            print("\n\n👋 Çıkılıyor...")
            exit(0)

# Kameraları bul ve seç
available_cameras = find_available_cameras()
selected_camera = select_camera(available_cameras)

print(f"\n✅ Seçilen kamera: Kamera {selected_camera['index']} ({selected_camera['backend_name']})")
print()

# Seçilen kamerayı aç
cap = cv2.VideoCapture(selected_camera['index'], selected_camera['backend'])

if not cap.isOpened():
    print("❌ Seçilen kamera açılamadı!")
    input("Çıkmak için Enter'a basın...")
    exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Test frame
ret, test_frame = cap.read()
if not ret or test_frame is None:
    print("❌ Kamera açıldı ama frame okunamıyor!")
    print("   Kamerayı başka bir uygulama kullanıyor olabilir.")
    cap.release()
    input("Çıkmak için Enter'a basın...")
    exit(1)

print(f"✅ Kamera başarıyla başlatıldı! ({test_frame.shape[1]}x{test_frame.shape[0]})")
print()

# Hand tracking
hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=1
)

def calculate_distance(point1, point2):
    """İki nokta arası mesafe hesapla"""
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def draw_info_panel(frame, thumb_pos, index_pos, ring_pos, distance_index, distance_ring, gesture, hand_side, drag_mode, click_mode):
    """Bilgi paneli çiz"""
    h, w, _ = frame.shape
    
    # Siyah panel - biraz daha büyük
    cv2.rectangle(frame, (10, 10), (450, 260), (0, 0, 0), -1)
    cv2.rectangle(frame, (10, 10), (450, 260), (0, 255, 255), 2)
    
    # Başlık
    cv2.putText(frame, "HAND TRACKING DEBUG", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    
    # Mesafe bilgileri
    color_index = (0, 255, 0) if distance_index < 60 else (255, 255, 255)
    cv2.putText(frame, f"Thumb-Index: {distance_index:.1f}px", (20, 75), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_index, 2)
    
    color_ring = (0, 255, 0) if distance_ring < 60 else (255, 255, 255)
    cv2.putText(frame, f"Thumb-Ring: {distance_ring:.1f}px", (20, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_ring, 2)
    
    # Gesture durumu
    cv2.putText(frame, f"Gesture: {gesture}", (20, 130), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0) if gesture != "NONE" else (255, 255, 255), 2)
    
    # El tarafı
    cv2.putText(frame, f"Hand Side: {hand_side}", (20, 160), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)
    
    # Click mode
    click_color = (0, 255, 0) if click_mode else (100, 100, 100)
    cv2.putText(frame, f"Click Mode: {'ACTIVE' if click_mode else 'OFF'}", (20, 190), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, click_color, 2)
    
    # Drag mode
    drag_color = (0, 255, 0) if drag_mode else (100, 100, 100)
    cv2.putText(frame, f"Drag Mode: {'ACTIVE' if drag_mode else 'OFF'}", (20, 220), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, drag_color, 2)
    
    # Parmak pozisyonları
    cv2.putText(frame, f"Thumb: ({thumb_pos[0]:.0f}, {thumb_pos[1]:.0f})", (20, 245), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 191, 255), 1)
    cv2.putText(frame, f"Index: ({index_pos[0]:.0f}, {index_pos[1]:.0f})", (230, 245), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

print("\n" + "=" * 50)
print("🖐️  HAND TRACKING DEBUG TOOL")
print("=" * 50)
print("📋 Kullanım:")
print("   • Baş parmak + İşaret parmağı:")
print("     - Bir kere birleştir → Sol Click")
print("     - Basılı tut → Sürükle (Drag)")
print("   • Baş parmak + Yüzük parmağı:")
print("     - Birleştir → Mouse hareket ettir")
print("   • ESC tuşu ile çıkış")
print("=" * 50)
print()

# Drag mode değişkenleri
drag_mode = False
click_mode = False
last_hand_pos = None
last_click_time = 0
click_threshold = 0.5  # 500ms
is_dragging = False
screen_width, screen_height = pyautogui.size()
smoothing_factor = 0.3  # Yumuşak hareket için

while cap.isOpened():
    success, frame = cap.read()
    
    # Debug: Frame durumunu kontrol et
    if not success or frame is None:
        print(f"⚠️  Frame okunamadı! success={success}, frame={'None' if frame is None else 'OK'}")
        # Boş siyah frame göster
        frame = cv2.imread('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')
        if frame is None:
            frame = [[0] * 640 for _ in range(480)]
            frame = cv2.cvtColor(cv2.UMat(frame), cv2.COLOR_GRAY2BGR)
        cv2.putText(frame, "KAMERA HATASI - Frame okunamiyor!", (50, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow(f'Hand Tracking Debug - Kamera {selected_camera["index"]}', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
        continue
    
    print(f"✓ Frame OK: {frame.shape}")  # Debug
    
    # Aynalama
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    # ÖNCELİKLE FRAME'İ GÖSTER - MediaPipe'dan önce
    cv2.imshow(f'Hand Tracking Debug - Kamera {selected_camera["index"]}', frame)
    
    # ESC kontrolü - MediaPipe'dan önce
    if cv2.waitKey(1) & 0xFF == 27:
        break
    
    # RGB'ye çevir
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    thumb_pos = (0, 0)
    index_pos = (0, 0)
    ring_pos = (0, 0)
    distance_index = 0
    distance_ring = 0
    gesture = "NONE"
    hand_side = "NONE"
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # El iskeletini çiz (kırmızı noktalar ve beyaz çizgiler)
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
            
            # Parmak uçları
            thumb = hand_landmarks.landmark[4]      # Baş parmak
            index_finger = hand_landmarks.landmark[8]  # İşaret parmağı
            ring_finger = hand_landmarks.landmark[16]  # Yüzük parmağı
            wrist = hand_landmarks.landmark[9]      # El merkezi
            
            # Piksel koordinatlarına çevir
            thumb_pos = (int(thumb.x * w), int(thumb.y * h))
            index_pos = (int(index_finger.x * w), int(index_finger.y * h))
            ring_pos = (int(ring_finger.x * w), int(ring_finger.y * h))
            wrist_pos = (int(wrist.x * w), int(wrist.y * h))
            
            # Mesafeleri hesapla
            distance_index = calculate_distance(thumb_pos, index_pos)
            distance_ring = calculate_distance(thumb_pos, ring_pos)
            
            # Ekstra vurgulu çizim
            # Baş parmak - Cyan
            cv2.circle(frame, thumb_pos, 15, (255, 255, 0), -1)
            cv2.circle(frame, thumb_pos, 18, (255, 255, 0), 3)
            cv2.putText(frame, "THUMB", (thumb_pos[0] - 30, thumb_pos[1] - 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            
            # İşaret parmağı - Yeşil
            cv2.circle(frame, index_pos, 15, (0, 255, 0), -1)
            cv2.circle(frame, index_pos, 18, (0, 255, 0), 3)
            cv2.putText(frame, "INDEX", (index_pos[0] - 25, index_pos[1] - 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Yüzük parmak - Magenta
            cv2.circle(frame, ring_pos, 15, (255, 0, 255), -1)
            cv2.circle(frame, ring_pos, 18, (255, 0, 255), 3)
            cv2.putText(frame, "RING", (ring_pos[0] - 20, ring_pos[1] - 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
            
            # Baş parmak + İşaret parmağı → Click/Drag
            if distance_index < 60:  # 50'den 60'a çıkardık - daha hassas
                line_color = (0, 255, 0)
                cv2.line(frame, thumb_pos, index_pos, line_color, 3)
                
                mid_x = (thumb_pos[0] + index_pos[0]) // 2
                mid_y = (thumb_pos[1] + index_pos[1]) // 2
                cv2.putText(frame, f"{distance_index:.0f}", (mid_x, mid_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, line_color, 2)
                
                current_time = time.time()
                
                if not click_mode:
                    # İlk kez birleşti - Click yap
                    click_mode = True
                    last_click_time = current_time
                    pyautogui.mouseDown()
                    print("🖱️  LEFT CLICK DOWN")
                    gesture = "CLICK/DRAG"
                    
                    # Trigger efekti
                    cv2.circle(frame, (mid_x, mid_y), 30, (0, 255, 0), 3)
                    cv2.putText(frame, "CLICKING!", (mid_x - 60, mid_y + 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                else:
                    # Basılı tutuluyor - Drag mode
                    gesture = "DRAGGING"
                    is_dragging = True
                    
                    # El pozisyonunu ekran koordinatlarına çevir
                    hand_x_normalized = wrist.x
                    hand_y_normalized = wrist.y
                    
                    target_x = int(hand_x_normalized * screen_width)
                    target_y = int(hand_y_normalized * screen_height)
                    
                    # Yumuşak hareket
                    current_mouse_x, current_mouse_y = pyautogui.position()
                    smooth_x = int(current_mouse_x + (target_x - current_mouse_x) * smoothing_factor)
                    smooth_y = int(current_mouse_y + (target_y - current_mouse_y) * smoothing_factor)
                    
                    pyautogui.moveTo(smooth_x, smooth_y, duration=0)
                    
                    cv2.circle(frame, (mid_x, mid_y), 30, (0, 255, 0), 3)
                    cv2.putText(frame, "DRAGGING!", (mid_x - 60, mid_y + 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    # Cursor pozisyonu
                    cursor_x, cursor_y = pyautogui.position()
                    cv2.putText(frame, f"Cursor: ({cursor_x}, {cursor_y})", (w - 250, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            else:
                # Parmaklar ayrıldı - Click'i bırak
                if click_mode:
                    pyautogui.mouseUp()
                    click_mode = False
                    is_dragging = False
                    print("🖱️  LEFT CLICK UP")
            
            # Baş parmak + Yüzük parmağı → Mouse hareket
            if distance_ring < 60 and distance_index > 60:  # 50'den 60'a çıkardık
                line_color = (255, 0, 255)
                cv2.line(frame, thumb_pos, ring_pos, line_color, 3)
                
                mid_x = (thumb_pos[0] + ring_pos[0]) // 2
                mid_y = (thumb_pos[1] + ring_pos[1]) // 2
                cv2.putText(frame, f"{distance_ring:.0f}", (mid_x, mid_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, line_color, 2)
                
                gesture = "MOVE MOUSE"
                
                if not drag_mode:
                    drag_mode = True
                    last_hand_pos = wrist_pos
                    print("🖱️  MOUSE MOVE MODE")
                
                # El pozisyonunu ekran koordinatlarına çevir
                hand_x_normalized = wrist.x
                hand_y_normalized = wrist.y
                
                target_x = int(hand_x_normalized * screen_width)
                target_y = int(hand_y_normalized * screen_height)
                
                # Yumuşak hareket
                current_mouse_x, current_mouse_y = pyautogui.position()
                smooth_x = int(current_mouse_x + (target_x - current_mouse_x) * smoothing_factor)
                smooth_y = int(current_mouse_y + (target_y - current_mouse_y) * smoothing_factor)
                
                pyautogui.moveTo(smooth_x, smooth_y, duration=0)
                
                last_hand_pos = wrist_pos
                
                cv2.circle(frame, (mid_x, mid_y), 30, (255, 0, 255), 3)
                cv2.putText(frame, "MOVING!", (mid_x - 50, mid_y + 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)
                
                cursor_x, cursor_y = pyautogui.position()
                cv2.putText(frame, f"Cursor: ({cursor_x}, {cursor_y})", (w - 250, 80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
            else:
                if drag_mode:
                    drag_mode = False
                    last_hand_pos = None
                    print("🖱️  MOUSE MOVE OFF")
    else:
        # El algılanmadı - Her şeyi kapat
        if drag_mode:
            drag_mode = False
            last_hand_pos = None
            print("🔴 MOUSE MOVE OFF - El algılanamadı")
        if click_mode:
            pyautogui.mouseUp()
            click_mode = False
            is_dragging = False
            print("🖱️  LEFT CLICK UP - El algılanamadı")
    
    # Bilgi panelini çiz
    draw_info_panel(frame, thumb_pos, index_pos, ring_pos, distance_index, distance_ring, gesture, hand_side, drag_mode, click_mode)
    
    # FPS göster
    cv2.putText(frame, "Press ESC to exit", (w - 200, h - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # Frame'i güncelle (zaten başta gösterildi, şimdi sadece güncelle)
    cv2.imshow(f'Hand Tracking Debug - Kamera {selected_camera["index"]}', frame)

cap.release()
cv2.destroyAllWindows()
hands.close()
print("\n✅ Hand tracking kapatıldı")
