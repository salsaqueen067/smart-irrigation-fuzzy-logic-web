# 🌱 Smart Irrigation System dengan Fuzzy Logic
Sistem Irigasi Cerdas berbasis IoT yang menggunakan Fuzzy Logic untuk mengoptimalkan penggunaan air.

## 📌 Fitur
- ✅ Monitoring sensor real-time (kelembaban tanah, suhu, kelembaban udara)
- ✅ Fuzzy Logic Controller dengan 27 aturan
- ✅ Dashboard interaktif dengan visualisasi data
- ✅ Kontrol penyiraman otomatis dan manual
- ✅ Rekomendasi durasi penyiraman optimal

## 🛠️ Teknologi
- **Backend:** Python 3.14.0 Flask
- **Algorithm:** Fuzzy Logic (Mamdani)
- **Frontend:** HTML5, CSS3, JavaScript
- **Styling:** Custom CSS dengan Gradient Design

## 🧮 Fuzzy Logic
Sistem menggunakan 3 input:
- Kelembaban Tanah (0-100%)
- Suhu Lingkungan (0-50°C)
- Kelembaban Udara (0-100%)
Output: Durasi Penyiraman (0-60 menit)

### Aturan Fuzzy (27 rules):
- Tanah Kering + Suhu Panas + Udara Kering → Siram Lama (40-50 menit)
- Tanah Lembab + Suhu Normal + Udara Sedang → Siram Sedang (20-30 menit)
- Tanah Basah + Suhu Dingin + Udara Lembab → Siram Singkat (10-15 menit)

## 📦 Instalasi
### 1. Clone Repository
```bash
git clone https://github.com/salsaqueen067/smart-irrigation-fuzzy-logic-web.git
cd smart-irrigation-fuzzy-logic-web
```

### 2. Buat Virtual Environment
```bash
# Windows
python -m venv myweb
myweb\Scripts\activate.bat

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi
```bash
python main.py
```

### 5. Buka Browser
```
http://localhost:5000
```

## 📂 Struktur Folder
```
smart-irrigation-fuzzy-logic-web/
│
├── templates/
│   └── index.html          # Template HTML dashboard
│
├── main.py                 # File utama Flask + Fuzzy Logic
├── requirements.txt        # Dependencies Python
├── .gitignore             # File yang diabaikan Git
└── README.md              # Dokumentasi project
```

## 🎯 Cara Penggunaan
1. **Mode Otomatis:** Klik "Gunakan Data Sensor Real-time" untuk menggunakan data simulasi sensor
2. **Mode Manual:** Input nilai sensor secara manual (kelembaban tanah, suhu, kelembaban udara)
3. **Hitung:** Klik "Hitung dengan Fuzzy Logic" untuk mendapat rekomendasi durasi penyiraman
4. **Kontrol:** Mulai atau hentikan penyiraman sesuai rekomendasi sistem

## 🔬 Metodologi Fuzzy Logic
### Tahapan:
1. **Fuzzifikasi:** Konversi nilai crisp (angka) ke nilai fuzzy (linguistik)
2. **Inference:** Evaluasi 27 aturan if-then untuk decision making
3. **Defuzzifikasi:** Metode Centroid (Weighted Average) untuk menghasilkan output crisp

### Fungsi Keanggotaan:
- **Kelembaban Tanah:** Low (0-40%), Medium (20-60%), High (40-100%)
- **Suhu:** Cold (0-25°C), Normal (15-35°C), Hot (25-50°C)
- **Kelembaban Udara:** Low (0-50%), Medium (30-70%), High (50-100%)
- **Output Durasi:** Short (0-20 menit), Medium (10-40 menit), Long (20-60 menit)

## 👨‍💻 Pengembang
Tugas Akhir Mata Kuliah Sistem Cerdas

## 🙏 Acknowledgments
- Flask Framework
- NumPy Library
- Fuzzy Logic Theory
