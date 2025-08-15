# CallCenterBackend

CallCenterBackend, çağrı merkezi işlemlerini yönetmek için geliştirilmiş bir backend uygulamasıdır. FastAPI ile yazılmıştır ve temel olarak müşteri, abonelik, fatura, paket, problem, servis satın alma gibi işlemleri API üzerinden sunar.

## Özellikler
- Müşteri ve kullanıcı yönetimi
- Abonelik ve paket işlemleri
- Fatura ve fatura kalemi yönetimi
- Servis satın alma ve kalan kullanım takibi
- Problem ve çağrı log yönetimi
- Hata yönetimi ve özel middleware
- Gelişmiş loglama

## Kurulum
1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/Cevrimicii/CallCenterBackend.git
   ```
2. Proje dizinine girin:
   ```bash
   cd CallCenterBackend
   ```
3. Python sanal ortamı oluşturun ve etkinleştirin:
   ```bash
   python -m venv venvv
   venvv\Scripts\activate
   ```
4. Gereksinimleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

## Çalıştırma
Ana dosyayı FastAPI ile başlatmak için:
```bash
uvicorn main:app --reload
```

## Klasör Yapısı
- `main.py`: Uygulamanın giriş noktası
- `app/`: Uygulama kodları
  - `models/`: Veri modelleri
  - `routes/`: API endpointleri
  - `crud/`: CRUD işlemleri
  - `db/`: Veritabanı bağlantı ve yapılandırması
  - `middleware/`: Orta katmanlar (ör. hata yönetimi)
  - `utils/`: Yardımcı fonksiyonlar ve dekoratörler
- `logs/`: Uygulama log dosyaları
- `venvv/`: Sanal ortam


## Lisans
Bu proje MIT lisansı ile lisanslanmıştır.
