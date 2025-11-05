import json 
from pywinauto import Desktop 
from pywinauto.findwindows import ElementNotFoundError

# Aranacak pencerenin bilinen başlığı (farklı diller için de bulunabilir) # Benzer bir başlık kullanın örneğin: "Live Captions"
PENCERE_BASLIGI_ARAMASI = "Canlı Alt Yazılar" 

print(f"'{PENCERE_BASLIGI_ARAMASI}' penceresi aranıyor...")
print("Lütfen script çalışırken Canlı Alt Yazıları (Ctrl+Win+L) AÇIK tutun.")

config_data = {}

try:
    desk = Desktop(backend="uia")
    main_window = desk.window(title=PENCERE_BASLIGI_ARAMASI)
    print("Pencere başarıyla bulundu.")
    
    all_elements = main_window.descendants()
    
    found_element = None
    for elem in all_elements:
        try:
            info = elem.element_info

            if (info.control_type == "Text" and 
                "Caption" in info.automation_id):
                
                found_element = elem
                break
        except Exception:
            continue

    if found_element:
        config_data = {
            "window_title": main_window.element_info.name,
            "caption_auto_id": found_element.element_info.automation_id
        }
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
            
        print("\n--- KEŞİF BAŞARILI! ---")
        print(f"Bulunan Pencere Başlığı: {config_data['window_title']}")
        print(f"Bulunan Metin Alanı ID'si: {config_data['caption_auto_id']}")
        print("\nAyarlar 'config.json' dosyasına kaydedildi.")
        print("Artık 'main.py' script'ini çalıştırabilirsiniz.")

    else:
        print("HATA: Metin alanı (CaptionsTextBlock) bulunamadı.")

except ElementNotFoundError:
    print(f"HATA: '{PENCERE_BASLIGI_ARAMASI}' başlıklı pencere bulunamadı.")
except Exception as e:
    print(f"Beklenmedik bir hata oluştu: {e}")

print("\nÇıkmak için Enter'a basın...")
input()