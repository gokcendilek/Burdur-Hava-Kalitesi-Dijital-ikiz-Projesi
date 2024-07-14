import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Excel dosyasını okuma
file_path = 'burdur.xlsx'
df = pd.read_excel(file_path, skiprows=1, decimal=',', thousands='.')

# Sütun adlarını yeniden adlandırma
df.columns = ['Tarih', 'PM10 (µg/m³)', 'PM2.5 (µg/m³)', 'SO2 (µg/m³)', 'CO (µg/m³)', 'NO2 (µg/m³)', 'NOX (µg/m³)', 'NO (µg/m³)', 'O3 (µg/m³)']


# Tarih sütununu datetime formatına çevirme
df['Tarih'] = pd.to_datetime(df['Tarih'], format='%d.%m.%Y %H:%M:%S')

# `-` işaretlerini `NaN` ile değiştirme
df.replace('-', np.nan, inplace=True)

# Sayısal değerleri içeren sütunları dönüştürme
numeric_columns = ['PM10 (µg/m³)', 'PM2.5 (µg/m³)', 'SO2 (µg/m³)', 'CO (µg/m³)', 'NO2 (µg/m³)', 'NOX (µg/m³)', 'NO (µg/m³)', 'O3 (µg/m³)']
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)

# Eksik verileri ortalama ile doldurma
df.fillna(df.mean(), inplace=True)

# SO2 sınıflandırma fonksiyonu
def classify_SO2(value):
    if value <= 50:
        return 'İyi'
    elif 50 < value <= 100:
        return 'Orta'
    elif 100 < value <= 150:
        return 'Hassas'
    elif 150 < value <= 200:
        return 'Sağlıksız'
    elif 200 < value <= 300:
        return 'Kötü'
    else:
        return 'Tehlikeli'

# NO2 sınıflandırma fonksiyonu
def classify_NO2(value):
    if value <= 100:
        return 'İyi'
    elif 100 < value <= 250:
        return 'Orta'
    elif 250 < value <= 500:
        return 'Hassas'
    elif 500 < value <= 850:
        return 'Sağlıksız'
    elif 850 < value <= 1100:
        return 'Kötü'
    else:
        return 'Tehlikeli'

# CO sınıflandırma fonksiyonu
def classify_CO(value):
    if value <= 100:
        return 'İyi'
    elif 100 < value <= 200:
        return 'Orta'
    elif 200 < value <= 500:
        return 'Hassas'
    elif 500 < value <= 1000:
        return 'Sağlıksız'
    elif 1000 < value <= 2000:
        return 'Kötü'
    else:
        return 'Tehlikeli'

# O3 sınıflandırma fonksiyonu
def classify_O3(value):
    if value <= 120:
        return 'İyi'
    elif 120 < value <= 160:
        return 'Orta'
    elif 160 < value <= 180:
        return 'Hassas'
    elif 180 < value <= 240:
        return 'Sağlıksız'
    elif 240 < value <= 700:
        return 'Kötü'
    else:
        return 'Tehlikeli'

# PM10 sınıflandırma fonksiyonu
def classify_PM10(value):
    if value <= 50:
        return 'İyi'
    elif 50 < value <= 100:
        return 'Orta'
    elif 100 < value <= 260:
        return 'Hassas'
    elif 260 < value <= 400:
        return 'Sağlıksız'
    elif 400 < value <= 520:
        return 'Kötü'
    else:
        return 'Tehlikeli'


# Her bir veri noktası için SO2 sınıflandırmasını uygulama
df['SO2_Kalite'] = df['SO2 (µg/m³)'].apply(classify_SO2)
df['NO2_Kalite'] = df['NO2 (µg/m³)'].apply(classify_NO2)
df['CO_Kalite'] = df['CO (µg/m³)'].apply(classify_CO)
df['O3_Kalite'] = df['O3 (µg/m³)'].apply(classify_O3)
df['PM10_Kalite'] = df['PM10 (µg/m³)'].apply(classify_PM10)

# Genel hava kalitesini belirleme
df['Genel_Kalite'] = df[['SO2_Kalite', 'NO2_Kalite', 'CO_Kalite', 'O3_Kalite', 'PM10_Kalite']].apply(lambda x: x.mode()[0], axis=1)

# Veri setini gözden geçirme
print(df.head())






# Excel dosyasını kaydetme
df.to_excel('veriler_with_status1.xlsx', index=False)


# Sınıflandırmaların dağılımını gösteren grafikler
fig, axs = plt.subplots(3, 2, figsize=(14, 18))

# SO2
sns.countplot(x='SO2_Kalite', data=df, order=['İyi', 'Orta', 'Hassas', 'Sağlıksız', 'Kötü', 'Tehlikeli'], ax=axs[0, 0])
axs[0, 0].set_title('SO2 Kalite Dağılımı')
axs[0, 0].set_xlabel('Kalite')
axs[0, 0].set_ylabel('Sayı')

# NO2
sns.countplot(x='NO2_Kalite', data=df, order=['İyi', 'Orta', 'Hassas', 'Sağlıksız', 'Kötü', 'Tehlikeli'], ax=axs[0, 1])
axs[0, 1].set_title('NO2 Kalite Dağılımı')
axs[0, 1].set_xlabel('Kalite')
axs[0, 1].set_ylabel('Sayı')

# CO
sns.countplot(x='CO_Kalite', data=df, order=['İyi', 'Orta', 'Hassas', 'Sağlıksız', 'Kötü', 'Tehlikeli'], ax=axs[1, 0])
axs[1, 0].set_title('CO Kalite Dağılımı')
axs[1, 0].set_xlabel('Kalite')
axs[1, 0].set_ylabel('Sayı')

# O3
sns.countplot(x='O3_Kalite', data=df, order=['İyi', 'Orta', 'Hassas', 'Sağlıksız', 'Kötü', 'Tehlikeli'], ax=axs[1, 1])
axs[1, 1].set_title('O3 Kalite Dağılımı')
axs[1, 1].set_xlabel('Kalite')
axs[1, 1].set_ylabel('Sayı')

# PM10
sns.countplot(x='PM10_Kalite', data=df, order=['İyi', 'Orta', 'Hassas', 'Sağlıksız', 'Kötü', 'Tehlikeli'], ax=axs[2, 0])
axs[2, 0].set_title('PM10 Kalite Dağılımı')
axs[2, 0].set_xlabel('Kalite')
axs[2, 0].set_ylabel('Sayı')

# Genel Kalite
sns.countplot(x='Genel_Kalite', data=df, order=['İyi', 'Orta', 'Hassas', 'Sağlıksız', 'Kötü', 'Tehlikeli'], ax=axs[2, 1])
axs[2, 1].set_title('Genel Kalite Dağılımı')
axs[2, 1].set_xlabel('Kalite')
axs[2, 1].set_ylabel('Sayı')

plt.tight_layout()
plt.show()


# Zaman serisi grafiği
plt.figure(figsize=(12, 6))
plt.plot(df['Tarih'], df['Genel_Kalite'])
plt.title('Zaman Serisi Hava Kalitesi')
plt.xlabel('Tarih')
plt.ylabel('Hava Kalitesi')
plt.xticks(rotation=45)
plt.show()
















# PM10 ve PM2.5 zaman serisi plotu
plt.figure(figsize=(12, 6))
plt.plot(df['Tarih'], df['PM10 (µg/m³)'], label='PM10 (µg/m³)')
plt.plot(df['Tarih'], df['PM2.5 (µg/m³)'], label='PM2.5 (µg/m³)', color='orange')
plt.xlabel('Tarih')
plt.ylabel('Konsantrasyon (µg/m³)')
plt.title('PM10 ve PM2.5 Zaman Serisi')
plt.legend()
plt.show()

# Her bir parametrenin istatistiksel özelliklerini hesaplamak için gruplama
istatistikler = df.describe()

# İstatistiksel özelliklerin sadece min, max, std ve ortalama değerlerini alalım
istatistikler = istatistikler.loc[['min', 'max', 'std', 'mean']]

# Sonucu ekrana daha geniş bir şekilde yazdıralım
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(istatistikler)



# Tarih sütunundan ay bilgisini çıkarma
df['Ay'] = df['Tarih'].dt.month

# Yıl sütununu ekleyelim
df['Yil'] = df['Tarih'].dt.year

# Ay ve yıla göre gruplayalım
grouped = df.groupby(['Ay', 'Yil'])

# Ay ve yıla göre istatistiksel özellikleri hesaplayalım
aylik_istatistikler = grouped.agg({
    'PM10 (µg/m³)': ['min', 'max', 'mean', 'std'],
    'PM2.5 (µg/m³)': ['min', 'max', 'mean', 'std'],
    'SO2 (µg/m³)': ['min', 'max', 'mean', 'std'],
    'CO (µg/m³)': ['min', 'max', 'mean', 'std'],
    'NO2 (µg/m³)': ['min', 'max', 'mean', 'std'],
    'NOX (µg/m³)': ['min', 'max', 'mean', 'std'],
    'NO (µg/m³)': ['min', 'max', 'mean', 'std'],
    'O3 (µg/m³)': ['min', 'max', 'mean', 'std']
})
# Ekrana yazdıralım
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(aylik_istatistikler)

# Korelasyon matrisi oluşturma
correlation_matrix = df[numeric_columns].corr()

# Korelasyon matrisini görüntüleme
print(correlation_matrix)

# Isı haritası (heatmap) ile korelasyon matrisini görselleştirme
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Kirlilik Parametreleri Arasındaki Korelasyon')
plt.show()


# Korelasyonları tablo şeklinde yazdırma
correlation_table = correlation_matrix.unstack().reset_index()
correlation_table.columns = ['Parametre 1', 'Parametre 2', 'Korelasyon']
correlation_table = correlation_table[correlation_table['Parametre 1'] != correlation_table['Parametre 2']]
correlation_table = correlation_table.sort_values(by='Korelasyon', ascending=False).reset_index(drop=True)

yorum = """
Bu tablo, çeşitli hava kirleticiler arasındaki korelasyonları göstermektedir. Korelasyon katsayısı, iki değişken arasındaki doğrusal ilişkinin gücünü ve yönünü ifade eder ve -1 ile 1 arasında değişir. Pozitif bir değer, bir değişkenin artmasıyla diğerinin de arttığını, negatif bir değer ise bir değişkenin artmasıyla diğerinin azaldığını gösterir.

### PM10 ve Diğer Kirleticiler
- **PM10 ve PM2.5: Korelasyon katsayısı 0.715779. Bu, iki parçacık madde arasında güçlü bir pozitif ilişki olduğunu gösterir; yani, PM10 seviyeleri arttıkça, PM2.5 seviyeleri de artma eğilimindedir.
- **PM10 ve SO2: Korelasyon katsayısı 0.344598. Orta düzeyde pozitif bir ilişki var.
- **PM10 ve CO: Korelasyon katsayısı 0.394910. Orta düzeyde pozitif bir ilişki var.
- **PM10 ve NO2**: Korelasyon katsayısı 0.318405. Orta düzeyde pozitif bir ilişki var.
- **PM10 ve NOX**: Korelasyon katsayısı 0.338442. Orta düzeyde pozitif bir ilişki var.
- **PM10 ve NO**: Korelasyon katsayısı 0.348354. Orta düzeyde pozitif bir ilişki var.
- **PM10 ve O3**: Korelasyon katsayısı -0.141697. Zayıf negatif bir ilişki var; PM10 seviyeleri arttıkça, ozon (O3) seviyeleri azalma eğilimindedir.

### PM2.5 ve Diğer Kirleticiler
- **PM2.5 ve SO2**: Korelasyon katsayısı 0.538850. Orta düzeyde güçlü bir pozitif ilişki var.
- **PM2.5 ve CO**: Korelasyon katsayısı 0.545802. Orta düzeyde güçlü bir pozitif ilişki var.
- **PM2.5 ve NO2**: Korelasyon katsayısı 0.397469. Orta düzeyde pozitif bir ilişki var.
- **PM2.5 ve NOX**: Korelasyon katsayısı 0.439885. Orta düzeyde pozitif bir ilişki var.
- **PM2.5 ve NO**: Korelasyon katsayısı 0.471814. Orta düzeyde pozitif bir ilişki var.
- **PM2.5 ve O3**: Korelasyon katsayısı -0.250398. Orta düzeyde negatif bir ilişki var; PM2.5 seviyeleri arttıkça, ozon (O3) seviyeleri azalma eğilimindedir.

### Diğer Kirleticiler Arasındaki İlişkiler
- **SO2 ve CO**: Korelasyon katsayısı 0.595362. Orta düzeyde güçlü bir pozitif ilişki var.
- **SO2 ve NO2**: Korelasyon katsayısı 0.418663. Orta düzeyde pozitif bir ilişki var.
- **SO2 ve NOX**: Korelasyon katsayısı 0.459065. Orta düzeyde pozitif bir ilişki var.
- **SO2 ve NO**: Korelasyon katsayısı 0.462183. Orta düzeyde pozitif bir ilişki var.
- **SO2 ve O3**: Korelasyon katsayısı -0.229760. Orta düzeyde negatif bir ilişki var.
- **CO ve NO2**: Korelasyon katsayısı 0.718293. Güçlü bir pozitif ilişki var.
- **CO ve NOX**: Korelasyon katsayısı 0.749356. Güçlü bir pozitif ilişki var.
- **CO ve NO**: Korelasyon katsayısı 0.738995. Güçlü bir pozitif ilişki var.
- **CO ve O3**: Korelasyon katsayısı -0.278915. Orta düzeyde negatif bir ilişki var.
- **NO2 ve NOX**: Korelasyon katsayısı 0.973436. Çok güçlü bir pozitif ilişki var.
- **NO2 ve NO**: Korelasyon katsayısı 0.927275. Çok güçlü bir pozitif ilişki var.
- **NO2 ve O3**: Korelasyon katsayısı -0.418438. Orta düzeyde negatif bir ilişki var.
- **NOX ve NO**: Korelasyon katsayısı 0.968606. Çok güçlü bir pozitif ilişki var.
- **NOX ve O3**: Korelasyon katsayısı -0.375426. Orta düzeyde negatif bir ilişki var.
- **NO ve O3**: Korelasyon katsayısı -0.345193. Orta düzeyde negatif bir ilişki var.

Bu korelasyon matrisi, hava kirleticileri arasındaki ilişkilerin karmaşıklığını ve bazı kirleticilerin birbirleriyle pozitif ya da negatif ilişkiler içinde olduğunu göstermektedir. Bu bilgiler, hava kalitesi yönetimi ve kirlilik kontrol stratejilerinin geliştirilmesinde önemli olabilir.




"""

print(yorum)







