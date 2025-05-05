import cv2
import os
import numpy as np
from ultralytics import YOLO

# YOLO modelini yükle
model = YOLO('yolov8n.pt')

# Test edilecek görüntüleri yükle
test_dir = "dataset/0"  # 0 rakamının örneklerinin bulunduğu klasör

if not os.path.exists(test_dir):
    print("Test klasörü bulunamadı! Önce veri seti oluşturun.")
    exit()

# Test görüntülerini al
test_images = [os.path.join(test_dir, f) for f in os.listdir(test_dir) if f.endswith('.jpg')]

if not test_images:
    print("Test görüntüsü bulunamadı!")
    exit()

print(f"Toplam {len(test_images)} test görüntüsü bulundu.")

# Her görüntüyü test et
for img_path in test_images:
    # Görüntüyü yükle
    frame = cv2.imread(img_path)
    if frame is None:
        print(f"Görüntü yüklenemedi: {img_path}")
        continue

    # YOLO ile nesne tespiti
    results = model(frame)
    
    # Tespit edilen nesneleri görüntüye çiz
    annotated_frame = results[0].plot()
    
    # Tespit edilen nesneleri göster
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Sınıf ID'sini al
            cls = int(box.cls[0])
            # Güven skorunu al
            conf = float(box.conf[0])
            # Sadece yüksek güven skoruna sahip tespitleri göster
            if conf > 0.5:
                print(f"Görüntü: {os.path.basename(img_path)}")
                print(f"Tespit edilen sınıf: {cls}, Güven: {conf:.2f}")
                if cls == 0:
                    print("✅ 0 rakamı doğru tespit edildi!")
                else:
                    print("❌ Yanlış tespit!")

    # Görüntüyü göster
    cv2.imshow("Test Sonucu", annotated_frame)
    cv2.waitKey(0)  # Bir tuşa basana kadar bekle

cv2.destroyAllWindows()
print("\nTest tamamlandı!") 