import time
import os
import sys
import json 
import traceback
from pywinauto import Desktop 
from pywinauto.findwindows import ElementNotFoundError

# --- 1. CONFIG DOSYASINI OKU ---
try:
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    PENCERE_BASLIGI = config["window_title"]
    METIN_ALANI_ID = config["caption_auto_id"]
except FileNotFoundError:
    print("HATA: 'config.json' dosyası bulunamadı.")
    print("Lütfen önce 'python discover.py' script'ini çalıştırın.")
    input("Çıkmak için Enter'a basın...")
    sys.exit()
except KeyError:
    print("HATA: 'config.json' dosyası bozuk veya eksik.")
    print("Lütfen 'discover.py' script'ini yeniden çalıştırın.")
    input("Çıkmak için Enter'a basın...")
    sys.exit()

# --- 2. DOSYA ADI ARGÜMANINI OKU ---
if len(sys.argv) < 2:
    print("HATA: Çıktı için bir dosya adı belirtmediniz.")
    print("Doğru Kullanım: python main.py NOTLARIM.txt")
    input("Çıkmak için Enter'a basın...")
    sys.exit()

CIKTI_DOSYASI_HAM = sys.argv[1]
CIKTI_DOSYASI = CIKTI_DOSYASI_HAM if CIKTI_DOSYASI_HAM.endswith(".txt") else CIKTI_DOSYASI_HAM + ".txt"

# --- 3. SABİT AYARLAR ---
KONTROL_ARALIGI = 0.2 
CAPTURE_DELAY = 1.5  

# --- 4. ANA DÖNGÜ -

print(f"'{PENCERE_BASLIGI}' penceresine bağlanılıyor...")
print(f"Metin alanı ID'si: '{METIN_ALANI_ID}' (config'den okundu)")
print(f"Kayıtlar '{CIKTI_DOSYASI}' dosyasına eklenecek.")
print(f"Duraklama Gecikmesi: {CAPTURE_DELAY} saniye.")
print("Script'i durdurmak için CTRL+C tuşlarına basın.")

kaydedilen_satirlar = set()   
son_gorulen_metin = ""
son_degisiklik_zamani = time.time()
caption_element = None  

try:
    print("Masaüstü (Desktop) UIA backend'i başlatılıyor...")
    desk = Desktop(backend="uia")
    
    main_window = desk.window(title=PENCERE_BASLIGI)
    print("Pencere başarıyla bulundu.")
    
    print(f"'{METIN_ALANI_ID}' ID'li metin alanı aranıyor...")
    
    all_elements = main_window.descendants()
    
    for elem in all_elements:
        try:
            info = elem.element_info
            if (info.control_type == "Text" and 
                info.automation_id == METIN_ALANI_ID):
                caption_element = elem  
                print(f"'{METIN_ALANI_ID}' ID'li element başarıyla bulundu.")
                break  
        except Exception:
            continue

    if caption_element is None:
        raise ElementNotFoundError 
    
    print("Bağlantı başarılı! Metin dinleniyor...")
    
    son_gorulen_metin = caption_element.window_text() 
    son_degisiklik_zamani = time.time()

    while True:
        try:
            guncel_metin_blogu = caption_element.window_text()
            
            if guncel_metin_blogu != son_gorulen_metin:
                son_gorulen_metin = guncel_metin_blogu
                son_degisiklik_zamani = time.time()
            else:
                gecen_sure = time.time() - son_degisiklik_zamani
                
                if gecen_sure > CAPTURE_DELAY:
                    mevcut_satirlar = son_gorulen_metin.splitlines()
                    yeni_bisey_eklendi_mi = False
                    
                    with open(CIKTI_DOSYASI, "a", encoding="utf-8") as f:
                        for satir in mevcut_satirlar:
                            temiz_satir = satir.strip() 
                            if temiz_satir and temiz_satir not in kaydedilen_satirlar:
                                f.write(temiz_satir + "\n") 
                                kaydedilen_satirlar.add(temiz_satir)
                                yeni_bisey_eklendi_mi = True
                    
                    if yeni_bisey_eklendi_mi:
                        print(f"Yeni satırlar '{CIKTI_DOSYASI}' dosyasına kaydedildi.")
                        son_degisiklik_zamani = time.time()

            time.sleep(KONTROL_ARALIGI)

        except ElementNotFoundError:
            print("Hata: Canlı Alt Yazı penceresi kapandı. Script durduruluyor.")
            break
        except Exception as e:
            print(f"Döngü içinde bir hata oluştu: {e}")
            time.sleep(KONTROL_ARALIGI * 5) 

except ElementNotFoundError:
    print(f"HATA: '{PENCERE_BASLIGI}' başlıklı pencere bulunamadı veya element arama başarısız oldu.")
    print("Lütfen önce Canlı Alt Yazıları (Ctrl+Win+L) açın.")
except KeyboardInterrupt:
    print("\nScript kullanıcı tarafından durduruldu. Kayıt tamamlandı.")
except Exception as e:
    print(f"Başlangıçta kritik bir hata oluştu. Detaylar:")
    traceback.print_exc()

print("\nKayıt tamamlandı.")