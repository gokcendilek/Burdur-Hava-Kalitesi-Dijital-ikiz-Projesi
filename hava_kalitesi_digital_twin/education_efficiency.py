import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import random

# Rastgele veri üretme ve tahmin için gerekli modüller
from folium.plugins import MarkerCluster

# Veri yükleme
file_path = 'veriler_with_status1.xlsx'
df = pd.read_excel(file_path)

# Özellikler (X) ve hedef değişken (y) ayrımı
features = ['PM10 (µg/m³)', 'PM2.5 (µg/m³)', 'SO2 (µg/m³)', 'CO (µg/m³)', 'NO2 (µg/m³)', 'NOX (µg/m³)', 'NO (µg/m³)', 'O3 (µg/m³)']
X = df[features]
y = df['Genel_Kalite']

# Kategorik hedef değişkeni sayısal değerlere dönüştürme
quality_mapping = {'İyi': 0, 'Orta': 1, 'Hassas': 2, 'Sağlıksız': 3, 'Kötü': 4, 'Tehlikeli': 5}
y = y.map(quality_mapping)

# Veriyi eğitim ve test setlerine bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Random Forest modeli oluşturma ve eğitme
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Model ile tahmin yapma
y_pred = model.predict(X_test)

# Sınıflandırma raporu ve karışıklık matrisi
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=quality_mapping.keys(), yticklabels=quality_mapping.keys())
plt.xlabel('Tahmin Edilen')
plt.ylabel('Gerçek')
plt.show()

