import cv2
import os
import numpy as np
from datetime import datetime

# Veri seti klasörlerini oluştur
def create_dataset_folders():
    base_dir = "dataset"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Her rakam için bir klasör oluştur
    for i in range(10):
        digit_dir = os.path.join(base_dir, str(i))
        if not os.path.exists(digit_dir):
            os.makedirs(digit_dir)
    
    return base_dir

# Kamerayı başlat
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

# Veri seti klasörlerini oluştur
base_dir = create_dataset_folders()
current_digit = 0  # Şu an toplanan rakam (0-9)
saved_count = 0    # Her rakam için kaydedilen resim sayısı

print("Veri Seti Toplama Programı")
print("Kullanım:")
print("1. 0-9 arası bir rakam yazın")
print("2. 's' tuşuna basarak resmi kaydedin")
print("3. 'n' tuşuna basarak sonraki rakama geçin")
print("4. 'q' tuşuna basarak programdan çıkın")
print(f"\nŞu an toplanan rakam: {current_digit}")
print(f"Bu rakam için kaydedilen resim sayısı: {saved_count}")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Görüntü alınamadı!")
            break

        # ROI (Region of Interest) belirle - ekranın ortasında bir alan
        height, width = frame.shape[:2]
        roi = frame[height//4:3*height//4, width//4:3*width//4]
        
        # ROI'yi göster
        cv2.rectangle(frame, (width//4, height//4), (3*width//4, 3*height//4), (0, 255, 0), 2)
        
        # Bilgi metni
        cv2.putText(frame, f"Rakam: {current_digit}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Kaydedilen: {saved_count}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, "'s': Kaydet, 'n': Sonraki, 'q': Çık", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Görüntüyü göster
        cv2.imshow("Veri Seti Toplama", frame)
        
        # Klavye kontrolü
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # Resmi kaydet
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(base_dir, str(current_digit), f"{timestamp}.jpg")
            cv2.imwrite(filename, roi)
            saved_count += 1
            print(f"Resim kaydedildi: {filename}")
        elif key == ord('n'):
            # Sonraki rakama geç
            current_digit = (current_digit + 1) % 10
            saved_count = 0
            print(f"\nYeni rakam: {current_digit}")

except KeyboardInterrupt:
    print("\nProgram kullanıcı tarafından durduruldu.")
except Exception as e:
    print(f"Beklenmeyen hata: {str(e)}")
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Program sonlandırıldı.") 