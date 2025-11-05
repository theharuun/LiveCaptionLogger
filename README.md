# Windows Live Caption Logger (UIA)

Windows (11/10) "Canlı Alt Yazılar" (Live Captions) özelliğinden gelen metni OCR kullanmadan, doğrudan UIA (UI Automation) üzerinden yakalayıp bir `.txt` dosyasına kaydeden basit bir Python script'idir.

## Çözdüğü Problem

Çoğu tarayıcı eklentisi, üniversitelerin **LMS (Öğrenme Yönetim Sistemi)** veya **Perculus** gibi kapalı platformlarında çalışmaz. Bu script, platformdan (tarayıcı, uygulama vb.) bağımsız olarak, Windows seviyesinde çalıştığı için **herhangi bir uygulamadan** (canlı ders, oyun, video konferans) gelen sesi yazıya dökerek kaydedebilir.

## Özellikler (Neden Farklı?)

Bu proje, benzer araçlardan birkaç önemli özellikle ayrılır:

  *  **Yüksek Doğruluk (OCR'sız):** Metni ekran görüntüsü (OCR) ile değil, doğrudan Windows UIA elementinden okur. Bu sayede %100 doğrudur, CPU kullanmaz ve 2x hızdaki videolarda bile hatasız çalışır.
  *  **Akıllı Cümle Algılama:** Konuşmacı durakladığında bunu algılar ve sadece **tamamlanmış cümleleri** kaydeder. Ekrana kelime kelime akan metin yığınını değil, temiz bir transkript alırsınız.
  *  **Geleceğe Hazır (Dayanıklı):** `discover.py` script'i, Canlı Alt Yazı penceresinin teknik kimliklerini otomatik olarak tarar ve `config.json` dosyasına kaydeder. Microsoft, bir güncelleme ile arayüzü değiştirirse, kodun çökmesini engeller.
  *  **Dinamik Dosya Adı:** Kayıtlarınızı `python main.py ders_adi.txt` şeklinde ayrı ayrı dosyalara kaydetmenize olanak tanır.

## Gereksinimler

  * Python 3.x
  * Windows 10/11
  * `pywinauto` kütüphanesi

## Hızlı Başlangıç

### Adım 1: Kurulum ve Keşif (Sadece 1 Kez)

1.  **Projeyi klonlayın veya indirin.**
2.  **Gereksinimleri yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Keşif (Discover):**
    Bu adım, Canlı Alt Yazı penceresinin ve metin alanının teknik kimliklerini bulup `config.json` dosyasına kaydeder.
      * `Ctrl+Win+L` tuşlarına basarak Canlı Alt Yazıları açın.
      * Terminalden (Yönetici olarak) aşağıdaki komutu çalıştırın:
    <!-- end list -->
    ```bash
    python discover.py
    ```
      * `config.json` dosyanız başarıyla oluşturulacaktır.

### Adım 2: Kayıt (Log)

1.  Artık metni kaydetmeye hazırsınız.
2.  `Ctrl+Win+L` ile Canlı Alt Yazıları tekrar açın.
3.  Terminalden `main.py` script'ini ve **kaydetmek istediğiniz dosya adını** girin:
    ```bash
    python main.py ingilizce_dersi_notlari.txt
    ```
    veya
    ```bash
    python main.py pazartesi_toplantisi.txt
    ```
4.  Script, konuşmacı durakladıkça yeni cümleleri otomatik olarak `ingilizce_dersi_notlari.txt` dosyasına ekleyecektir.
5.  Durdurmak için terminalde `Ctrl+C` tuşlarına basın.

## Lisans

Bu proje MIT Lisansı altındadır.