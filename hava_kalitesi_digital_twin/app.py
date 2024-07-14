from flask import Flask, render_template, jsonify
import pandas as pd
import random
import time
from datetime import datetime
import threading
import os

app = Flask(__name__)

# Burdur ilçeleri ve koordinatları
ilceler = {
    'Merkez': (37.7205, 30.2909),
    'Altınyayla': (37.4508, 29.7056),
    'Bucak': (37.4590, 30.5878),
    'Çavdır': (37.0963, 29.6886),
    'Çeltikçi': (37.5736, 30.4604)
}

features = ['PM10 (µg/m³)', 'PM2.5 (µg/m³)', 'SO2 (µg/m³)', 'CO (µg/m³)', 'NO2 (µg/m³)', 'NOX (µg/m³)', 'NO (µg/m³)', 'O3 (µg/m³)']
output_columns = ['İlçe', 'PM10 (µg/m³)', 'PM2.5 (µg/m³)', 'SO2 (µg/m³)', 'CO (µg/m³)', 'NO2 (µg/m³)', 'NOX (µg/m³)', 'NO (µg/m³)', 'O3 (µg/m³)', 'Genel_Kalite_Tahmini', 'Tarih_Saat']

# Veri yükleme ve model eğitimi
file_path = 'veriler_with_status1.xlsx'
df = pd.read_excel(file_path)

# Özellikler (X) ve hedef değişken (y) ayrımı
X = df[features]
y = df['Genel_Kalite']

# Kategorik hedef değişkeni sayısal değerlere dönüştürme
quality_mapping = {'İyi': 0, 'Orta': 1, 'Hassas': 2, 'Sağlıksız': 3, 'Kötü': 4, 'Tehlikeli': 5}
y = y.map(quality_mapping)

# Veriyi eğitim ve test setlerine bölme
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Random Forest modeli oluşturma ve eğitme
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)



# Rastgele veri üretme fonksiyonu
def generate_random_data():
    global new_data_df
    while True:
        new_data_list = []
        for ilce, coords in ilceler.items():
            new_data = {
                'PM10 (µg/m³)': random.uniform(0, 600),
                'PM2.5 (µg/m³)': random.uniform(0, 600),
                'SO2 (µg/m³)': random.uniform(0, 1500),
                'CO (µg/m³)': random.uniform(0, 35000),
                'NO2 (µg/m³)': random.uniform(0, 1500),
                'NOX (µg/m³)': random.uniform(0, 1500),
                'NO (µg/m³)': random.uniform(0, 1500),
                'O3 (µg/m³)': random.uniform(0, 800)
            }
            new_data_df = pd.DataFrame([new_data])
            new_data_df['Genel_Kalite_Tahmini'] = model.predict(new_data_df)
            new_data['Genel_Kalite_Tahmini'] = int(new_data_df['Genel_Kalite_Tahmini'].iloc[0])
            new_data['İlçe'] = ilce
            new_data['Koordinatlar'] = coords
            new_data['Tarih_Saat'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            new_data_list.append(new_data)

        new_data_df = pd.DataFrame(new_data_list)
        
        # Yeni verileri CSV dosyasına ekleme
        new_data_df[output_columns].to_csv('new_air_quality_predictions.csv', mode='a', header=not os.path.exists('new_air_quality_predictions.csv'), index=False)

        time.sleep(15)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    return jsonify(new_data_df.to_dict(orient='records'))

if __name__ == '__main__':
    threading.Thread(target=generate_random_data).start()
    app.run(debug=True)
