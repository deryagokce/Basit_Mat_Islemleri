import cv2
import pytesseract
import re
import numpy as np
from ultralytics import YOLO

# Tesseract yolu
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\cihan bilgisayar\Documents\tesseract\tesseract.exe"

# YOLO modelini yükle
model = YOLO('yolov8n.pt')

def process_images():
    print("Resim işleme modu başlatıldı...")
    image_paths = ["toplama_ornek.png", "toplama_ornek2.png", "cikarma_ornek.png", "carpma_ornek.png", "bolme_ornek.png"]
    
    for image_path in image_paths:
        print(f"\nİşlenen görsel: {image_path}")
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"Hata: {image_path} bulunamadı!")
            continue
            
        # Görüntüyü göster
        cv2.imshow('Resim', image)
        cv2.waitKey(1000)  # 1 saniye bekle
        
        # OCR işlemi
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, config='--psm 6')
        print(f"Okunan metin: {text.strip()}")
        
        # Metni temizle ve işlemleri bul
        text = text.lower().strip()
        
        # Sayıları bul
        numbers = re.findall(r'\d+', text)
        if len(numbers) < 2:
            print("Yeterli sayı bulunamadı!")
            continue
            
        try:
            num1 = int(numbers[0])
            num2 = int(numbers[1])
            
            # Bölme işareti kontrolü - en önce kontrol et
            if ':' in text or '÷' in text or '/' in text or '\\' in text:
                if num2 != 0:
                    result = num1 / num2
                    print(f"Bölme: {num1} / {num2} = {result}")
                else:
                    print("Hata: Sıfıra bölme hatası!")
            # Çarpma işareti kontrolü
            elif '*' in text or 'x' in text or '×' in text or '·' in text:
                result = num1 * num2
                print(f"Çarpma: {num1} * {num2} = {result}")
            # Toplama işareti kontrolü
            elif '+' in text:
                result = num1 + num2
                print(f"Toplama: {num1} + {num2} = {result}")
            # Çıkarma işareti kontrolü
            elif '-' in text:
                result = num1 - num2
                print(f"Çıkarma: {num1} - {num2} = {result}")
            else:
                print("Matematiksel işlem bulunamadı!")
                
        except Exception as e:
            print(f"Hesaplama hatası: {e}")
    
    cv2.destroyAllWindows()

def start_camera():
    print("Kamera modu başlatıldı...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Kamera açılamadı!")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kamera görüntüsü alınamadı!")
            break
            
        # YOLO ile nesne tespiti
        results = model(frame)
        
        # Tespit edilen nesneleri işle
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Koordinatları al
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].cpu().numpy()
                
                if conf > 0.5:  # Güven eşiği
                    # Tespit edilen bölgeyi çerçevele
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    
                    # Tespit edilen bölgeyi al
                    roi = frame[int(y1):int(y2), int(x1):int(x2)]
                    
                    # Görüntü işleme - tüm işlemler için optimize
                    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    # Kontrast artırma
                    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)
                    # Gürültü azaltma
                    gray = cv2.GaussianBlur(gray, (3,3), 0)
                    # Eşikleme
                    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    # OCR işlemi - tüm işlemler için optimize
                    text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=0123456789+-*/()÷×·')
                    
                    # Metni temizle
                    text = text.strip()
                    print(f"Tespit edilen metin: {text}")  # Debug için
                    
                    # Sayıları bul
                    numbers = re.findall(r'\d+', text)
                    if len(numbers) >= 2:
                        try:
                            num1 = int(numbers[0])
                            num2 = int(numbers[1])
                            
                            # İşlem tespiti - daha esnek
                            if ':' in text or '÷' in text or '/' in text or '\\' in text or 'böl' in text.lower():
                                if num2 != 0:
                                    result = num1 / num2
                                    result_text = f"{num1} / {num2} = {result:.2f}"
                                    cv2.putText(frame, result_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                    print(f"Bölme: {result_text}")
                                else:
                                    print("Hata: Sıfıra bölme!")
                            elif '*' in text or 'x' in text or '×' in text or '·' in text or 'çarp' in text.lower():
                                result = num1 * num2
                                result_text = f"{num1} * {num2} = {result}"
                                cv2.putText(frame, result_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                print(f"Çarpma: {result_text}")
                            elif '+' in text or 'plus' in text.lower() or 'artı' in text.lower():
                                result = num1 + num2
                                result_text = f"{num1} + {num2} = {result}"
                                cv2.putText(frame, result_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                print(f"Toplama: {result_text}")
                            elif '-' in text or 'minus' in text.lower() or 'eksi' in text.lower():
                                result = num1 - num2
                                result_text = f"{num1} - {num2} = {result}"
                                cv2.putText(frame, result_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                print(f"Çıkarma: {result_text}")
                            
                        except Exception as e:
                            print(f"Hesaplama hatası: {e}")
        
        # Tüm ekranda OCR işlemi - tüm işlemler için optimize
        gray_full = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Kontrast artırma
        gray_full = cv2.convertScaleAbs(gray_full, alpha=1.5, beta=0)
        # Gürültü azaltma
        gray_full = cv2.GaussianBlur(gray_full, (3,3), 0)
        # Eşikleme
        _, thresh_full = cv2.threshold(gray_full, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        text_full = pytesseract.image_to_string(thresh_full, config='--psm 6 -c tessedit_char_whitelist=0123456789+-*/()÷×·')
        text_full = text_full.strip()
        print(f"Ekran metni: {text_full}")  # Debug için
        
        # Ekrandaki sayıları bul
        numbers_full = re.findall(r'\d+', text_full)
        if len(numbers_full) >= 2:
            try:
                num1 = int(numbers_full[0])
                num2 = int(numbers_full[1])
                
                # İşlem tespiti - daha esnek
                if ':' in text_full or '÷' in text_full or '/' in text_full or '\\' in text_full or 'böl' in text_full.lower():
                    if num2 != 0:
                        result = num1 / num2
                        result_text = f"Ekran: {num1} / {num2} = {result:.2f}"
                        cv2.putText(frame, result_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        print(f"Ekran Bölme: {result_text}")
                    else:
                        print("Hata: Sıfıra bölme!")
                elif '*' in text_full or 'x' in text_full or '×' in text_full or '·' in text_full or 'çarp' in text_full.lower():
                    result = num1 * num2
                    result_text = f"Ekran: {num1} * {num2} = {result}"
                    cv2.putText(frame, result_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    print(f"Ekran Çarpma: {result_text}")
                elif '+' in text_full or 'plus' in text_full.lower() or 'artı' in text_full.lower():
                    result = num1 + num2
                    result_text = f"Ekran: {num1} + {num2} = {result}"
                    cv2.putText(frame, result_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    print(f"Ekran Toplama: {result_text}")
                elif '-' in text_full or 'minus' in text_full.lower() or 'eksi' in text_full.lower():
                    result = num1 - num2
                    result_text = f"Ekran: {num1} - {num2} = {result}"
                    cv2.putText(frame, result_text, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    print(f"Ekran Çıkarma: {result_text}")
                
            except Exception as e:
                print(f"Ekran hesaplama hatası: {e}")
        
        # Görüntüyü göster
        cv2.imshow('Kamera', frame)
        
        # 'q' tuşuna basılırsa çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    print("\n=== Matematiksel İşlem Tanıma Programı ===")
    print("1. Resim işleme modu için 'r' tuşuna basın")
    print("2. Kamera modu için 'c' tuşuna basın")
    print("3. Çıkmak için 'q' tuşuna basın")
    
    while True:
        key = input("\nSeçiminiz (r/c/q): ").lower()
        
        if key == 'r':
            process_images()
        elif key == 'c':
            start_camera()
        elif key == 'q':
            print("Program sonlandırılıyor...")
            break
        else:
            print("Geçersiz seçim! Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
