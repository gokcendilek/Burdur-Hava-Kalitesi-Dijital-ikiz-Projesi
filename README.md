#  Burdur Hava Kalitesi Dijital İkiz Projesi

Bu proje, **Burdur ili ve ilçelerinin (Merkez, Altınyayla, Bucak, Çavdır, Çeltikçi)** hava kirliliği seviyelerini **gerçek zamanlı olarak izlemek, analiz etmek ve görselleştirmek** amacıyla geliştirilmiştir. Python kullanılarak geliştirilmiş bu sistem, hava kalitesi verilerini dinamik olarak işler ve **harita üzerinde renklerle anlık olarak gösterir.**

---

##  Amaç

- Burdur ve ilçelerinde hava kirliliği seviyelerini sürekli olarak izlemek  
- Gerçek zamanlı verileri analiz ederek vatandaşlara ve yöneticilere bilgi sunmak  
- Hava kalitesini görselleştirmek için dijital bir harita arayüzü oluşturmak  
- Anlık değişimlere göre harita renklerini otomatik güncellemek

---

##  Kullanılan Teknolojiler

- Python  
- `folium` veya `plotly` (Harita görselleştirmeleri için)  
- `pandas`, `numpy` (Veri işleme için)  
- `sqlite` ve `csv` (Veri kaydı için)  
-  Flask (opsiyonel kullanıcı arayüzü veya web arayüzü)

---

##  Özellikler
-  Önceki yıllardaki Burdur hava kalitesi verileri ile model eğitildi.
-  Her 5 saniyede bir verilerin güncellenmesi  
-  Burdur haritası üzerinde ilçelerin hava kalitesi seviyelerinin eğitilmiş modele göre değerlendirilerek renkle gösterimi  
- 🔴 Kötü hava kalitesi için kırmızı, 🟡 orta için sarı, 🟢 iyi için yeşil gibi renk kodlamaları  
- 📊 İlçelere göre detaylı PM2.5, PM10, CO, NO2 gibi kirlilik parametreleri

---

## 🔍 Harita Görselleştirme

Her ilçe için anlık hava kalitesi hesaplanır ve harita üzerinde aşağıdaki şekilde renklenir:

| Renk  | Hava Kalitesi Durumu |
|-------|----------------------|
| 🟢 Yeşil   | Temiz - Güvenli |
| 🟡 Sarı    | Orta - Dikkatli olunmalı |
| 🔴 Kırmızı | Kirli - Tehlikeli olabilir |

---

##  Başlatmak için

### 1. Depoyu klonlayın:
```bash
git clone https://github.com/yourusername/burdur-hava-kalitesi-dijital-ikiz.git
cd burdur-hava-kalitesi-dijital-ikiz

