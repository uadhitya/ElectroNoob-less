# ⚡ ElectroNoob-less: Independent Power Architect

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **"From Noob to Know"** — *Desain sistem energi mandiri (angin & surya) berdasarkan hukum fisika murni*

---

## 🎯 Apa Ini?

**ElectroNoob-less** adalah **Sistem Pakar (Expert System)** berbasis Python yang dirancang untuk membantu pemula maupun hobis merancang sistem pembangkit listrik mandiri (off-grid) yang menggabungkan:

- 🌬️ **Turbin Angin** dengan Generator Fluks Aksial (AFG - Axial Flux Generator)
- ☀️ **Panel Surya** Fotovoltaik
- 🔋 **Sistem Baterai** dengan perhitungan Depth of Discharge (DoD)
- ⚡ **Distribusi Daya** dengan analisis voltage drop dan efisiensi

Sistem ini **bukan simulator sederhana** — setiap perhitungan didasarkan pada **hukum fisika fundamental**:

| Hukum Fisika | Formula | Aplikasi dalam Sistem |
|--------------|---------|----------------------|
| **Faraday** | ε = -N × dΦ/dt | Desain generator AFG, perhitungan lilitan koil |
| **Ohm** | V = I × R | Voltage drop kabel, hambatan penghantar |
| **Joule** | P = I² × R | Pemanasan kabel, kehilangan energi |
| **Betz** | Cp ≤ 16/27 ≈ 0.593 | Batas efisiensi turbin angin maksimum |

---

## 🚀 Fitur Utama

### 1. 🌬️ Modul Angin & Generator AFG
- **Betz Limit Calculation**: Menghitung daya teoritis dan praktis dari turbin angin
- **Torque Analysis**: Analisis torsi pada berbagai RPM
- **Mechanical Transmission**: Perhitungan rasio reducer (pulley/gear)
- **AFG Design**: Desain generator fluks aksial dengan koil trapezoidal
  - Perhitungan lilitan berdasarkan magnet N52 (Br = 1.48 T)
  - Estimasi resistansi koil dan panas yang dihasilkan

### 2. ☀️ Modul Surya & Baterai
- **Battery Sizing**: Perhitungan kapasitas Ah berdasarkan:
  - Kebutuhan energi harian
  - Hari otonomi (1-5 hari)
  - Depth of Discharge (DoD): 50% untuk Lead Acid, 90% untuk LiFePO4
- **Solar Panel Recommendation**: Rekomendasi Watt-Peak panel untuk recharge dalam 2 hari cerah

### 3. 🎯 System Advisor
- **Voltage Drop Analysis**: Perhitungan kehilangan tegangan pada kabel (Ohm's Law)
- **Inverter Loss**: Perhitungan efisiensi konversi DC→AC (85% default)
- **Auto-Recommendation**: Saran otomatis untuk upgrade tegangan sistem jika voltage drop > 10%
- **System Balance Check**: Verifikasi keseimbangan antara generasi dan beban

### 4. 🔍 Physical Reality Check
Sebelum Anda membeli komponen, sistem akan memberitahu:
- ✅ **POSSIBLE**: Desain dapat dibangun secara fisik
- ⚠️ **CHALLENGING**: Desain mungkin tapi memerlukan perhatian khusus
- 🚨 **IMPOSSIBLE**: Desain melanggar batasan fisika atau praktis

### 5. 📚 Physics Insights (The 'Noob-less' Part)
Setiap modul dilengkapi dengan penjelasan teori fisika yang relevan:
- Penjelasan konsep dengan bahasa yang mudah dipahami
- Formula matematis yang digunakan
- Aplikasi praktis dalam desain sistem

---

## 📱 Mobile-First Design

Aplikasi ini dirancang dengan pendekatan **Mobile-First**:

- 📲 **Responsive Layout**: UI yang nyaman di smartphone maupun desktop
- 🎨 **Traffic Light System**: Indikator visual (Hijau/Kuning/Merah) untuk status sistem
- 📊 **st.metric**: Tampilan metrik utama yang jelas dan ringkas
- 📖 **st.expander**: Penjelasan teori yang bisa dilipat untuk menghemat ruang layar
- 🎚️ **Touch-Friendly Sliders**: Input yang mudah digunakan di layar sentuh

---

## 🛠️ Instalasi & Penggunaan

### Prasyarat
- Python 3.8 atau lebih baru
- pip package manager

### Instalasi

```bash
# Clone repository
git clone https://github.com/username/electronoob-less.git
cd electro-noobless

# Buat virtual environment (recommended)
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada alamat `http://localhost:8501`

---

## 📖 Cara Penggunaan

### 1. Input Parameter (Sidebar)

| Parameter | Rentang | Deskripsi |
|-----------|---------|-----------|
| **Kecepatan Angin** | 0-30 m/s | Kecepatan angin rata-rata di lokasi |
| **Jam Matahari** | 0-12 jam | Jam sinar puncak per hari |
| **Watt Total** | 1-10,000 W | Total daya semua perangkat |
| **Durasi Pakai** | 0.5-24 jam | Lama penggunaan per hari |
| **Jarak Kabel** | 1-100 m | Jarak dari sumber ke beban |
| **Hari Otonom** | 1-5 hari | Cadangan energi tanpa sinar/angin |
| **Tegangan Sistem** | 5/12/24/48/220V | Target tegangan operasi |
| **Jenis Baterai** | Lead Acid / LiFePO4 | Tipe baterai penyimpanan |

### 2. Analisis Output

Sistem akan menampilkan:
1. **Reality Check**: Apakah desain layak dibangun?
2. **Metrik Utama**: Daya angin, kapasitas baterai, rekomendasi panel
3. **Detail Teknis**: Perhitungan torsi, lilitan koil, voltage drop
4. **Rekomendasi**: Saran perbaikan jika ada masalah

### 3. Interpretasi Traffic Light

| Warna | Arti | Tindakan |
|-------|------|----------|
| 🟢 **Hijau** | Aman/Optimal | Lanjutkan desain |
| 🟡 **Kuning** | Peringatan | Pertimbangkan modifikasi |
| 🔴 **Merah** | Bahaya/Kritis | Wajib perbaiki sebelum lanjut |

---

## 🔬 Dasar Ilmiah

### 1. Limit Betz untuk Turbin Angin

Tidak ada turbin angin yang bisa mengkonversi lebih dari **59.3%** energi kinetik angin menjadi energi mekanik. Ini adalah batas fundamental dari hukum termodinamika:

```
Cp_max = 16/27 ≈ 0.593
```

Turbin komersial mencapai Cp = 0.35-0.45. Desain yang mengklaim efisiensi lebih tinggi adalah **fisikanya mustahil**.

### 2. Hukum Faraday untuk Generator

Tegangan yang diinduksi dalam kumparan:

```
ε = -N × dΦ/dt
```

Di mana:
- ε = tegangan induksi (Volt)
- N = jumlah lilitan
- dΦ/dt = laju perubahan fluks magnet (Weber/detik)

### 3. Hukum Ohm untuk Voltage Drop

Kehilangan tegangan pada kabel:

```
V_drop = I × R = I × (ρ × L / A)
```

Ini mengapa sistem 48V lebih efisien dari 12V untuk daya yang sama — arus lebih kecil, voltage drop lebih sedikit.

### 4. Hukum Joule untuk Pemanasan

Energi yang hilang sebagai panas:

```
P_heat = I² × R
```

**Penting**: Menggandakan arus → **empat kali lipat** panas! Ini mengapa kabel untuk 220V bisa lebih tipis dari 12V.

---

## 📊 Contoh Kasus

### Kasus 1: Sistem 12V untuk Rumah Kecil

**Input:**
- Beban: 100W × 8 jam = 800 Wh/hari
- Angin: 5 m/s
- Matahari: 5 jam/hari
- Autonomi: 2 hari
- Jarak kabel: 10m

**Output:**
- Baterai: ~170 Ah @ 12V (Lead Acid)
- Panel: 200 Wp (2×100W)
- Voltage drop: ~3.5% (aman)
- Status: ✅ POSSIBLE

### Kasus 2: Sistem 220V dengan Jarak Jauh

**Input:**
- Beban: 1000W × 6 jam
- Jarak kabel: 50m
- Tegangan: 12V

**Output:**
- Arus: 83A
- Voltage drop: 45% 🚨
- Rekomendasi: **Upgrade ke 48V atau gunakan kabel 16mm²**

---

## 🧪 Validasi & Verifikasi

Perhitungan dalam sistem ini divalidasi dengan:

1. **Referensi Akademik**:
   - Manwell, J.F., et al. "Wind Energy Explained" (Wiley, 2010)
   - Masters, G.M. "Renewable and Efficient Electric Power Systems" (Wiley, 2013)

2. **Standar Industri**:
   - IEC 61400 untuk turbin angin
   - IEEE 1547 untuk interkoneksi sistem

3. **Data Material**:
   - Resistivitas tembaga: 1.68×10⁻⁸ Ω·m @ 20°C
   - Remanence magnet N52: 1.48 Tesla
   - Densitas udara: 1.225 kg/m³ @ sea level

---

## 🚧 Batasan & Asumsi

### Asumsi Teknis:
1. **Turbin Angin**: Tip Speed Ratio (TSR) = 6 (optimal untuk horizontal axis)
2. **Generator AFG**: 12 pole pairs, magnet N52 20×20×10mm
3. **Panel Surya**: Efisiensi 18%, charge controller 85%
4. **Inverter**: Efisiensi 85% untuk 220V AC

### Batasan:
- Tidak memperhitungkan efek temperatur ekstrem pada baterai
- Asumsi kondisi angin dan matahari konstan (tidak real-time)
- Tidak termasuk analisis ekonomi/ROI
- Sistem DC sederhana (tidak termasuk MPPT canggih)

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Area yang bisa dikembangkan:

- [ ] Analisis ekonomi (CAPEX/OPEX)
- [ ] Database komponen komersial
- [ ] Visualisasi 3D turbin dan generator
- [ ] Integrasi data cuaca real-time (API)
- [ ] Simulasi dinamis (bukan steady-state)
- [ ] Multi-language support

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 ElectroNoob-less Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Kredit & Referensi

### Buku & Paper:
- Manwell, J.F., McGowan, J.G., Rogers, A.L. (2010). *Wind Energy Explained: Theory, Design and Application*. Wiley.
- Masters, G.M. (2013). *Renewable and Efficient Electric Power Systems*. Wiley-IEEE Press.
- Piggott, H. (2010). *A Wind Turbine Recipe Book*. Scoraig Wind Electric.

### Online Resources:
- [Wind Power Engineering](https://www.windpowerengineering.com)
- [Solar Power World](https://www.solarpowerworldonline.com)
- [Battery University](https://batteryuniversity.com)

### Tools & Libraries:
- [Streamlit](https://streamlit.io) - Web app framework
- [NumPy](https://numpy.org) - Numerical computing

---

## 📧 Kontak & Dukungan

Untuk pertanyaan, bug report, atau diskusi teknis:

- 📧 Email: [your-email@example.com]
- 💬 GitHub Issues: [https://github.com/username/electronoob-less/issues]
- 🌐 Website: [https://your-website.com]

---

## ⭐ Apresiasi

Jika proyek ini membantu Anda, berikan ⭐ di GitHub!

<p align="center">
  <i>"Knowledge is power — literally!" ⚡</i>
</p>

---

<p align="center">
  <b>ElectroNoob-less</b> — From Noob to Know
  <br>
  <sub>Built with ❤️ and Physics</sub>
</p>
