import cv2
import pytesseract
import re
import numpy as np

# Tesseract yolu
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\cihan bilgisayar\Documents\tesseract\tesseract.exe"

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
            
        # Görüntüyü göster
        cv2.imshow('Kamera', frame)
        
        # OCR işlemi
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray, config='--psm 6')
        
        # Metni temizle ve işlemleri bul
        text = text.lower().strip()
        
        # Sayıları bul
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
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
                
            except Exception as e:
                print(f"Hesaplama hatası: {e}")
        
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
