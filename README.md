# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan

- **Nama:** Sutriadi Kurniawan
- **Email:** sutriadik@gmail.com
- **ID Dicoding:** sutriadi_kurniawan

---

## Business Understanding

Jaya Jaya Institut adalah perguruan tinggi yang telah beroperasi sejak tahun 2000 dan saat ini menghadapi tantangan serius berupa tingginya angka dropout mahasiswa yang mencapai **32.1%** — hampir sepertiga dari seluruh mahasiswa terdaftar tidak menyelesaikan pendidikannya.

Tingginya angka dropout berdampak langsung pada berbagai aspek institusi:
- **Akreditasi & reputasi** — angka kelulusan yang rendah mempengaruhi penilaian akreditasi dan citra institusi di mata calon mahasiswa maupun masyarakat
- **Operasional & finansial** — biaya rekrutmen mahasiswa baru yang terus meningkat untuk menggantikan yang keluar, serta kehilangan potensi pendapatan dari mahasiswa yang tidak menyelesaikan studi
- **Kualitas lulusan** — tingginya dropout mengindikasikan adanya permasalahan sistemik pada dukungan akademik, finansial, maupun sosial yang diberikan institusi

Selama ini, identifikasi mahasiswa berisiko dropout dilakukan secara reaktif — setelah mahasiswa sudah terlanjur keluar. Institusi belum memiliki mekanisme deteksi dini yang mampu mengidentifikasi mahasiswa berisiko sejak semester pertama, sehingga intervensi sering terlambat dan tidak tepat sasaran.

Proyek ini membangun solusi berbasis machine learning sebagai tools **deteksi dini dropout** yang dapat membantu tim akademik dan konseling mengidentifikasi mahasiswa berisiko secara proaktif, sehingga intervensi dapat dirancang lebih tepat waktu dan tepat sasaran sebelum mahasiswa benar-benar keluar.

### Permasalahan Bisnis

1. Faktor apa yang paling memengaruhi mahasiswa untuk dropout?
2. Bisakah kita memprediksi mahasiswa yang berisiko dropout sedini mungkin?
3. Intervensi apa yang dapat dilakukan untuk mengurangi angka dropout secara efektif?

### Cakupan Proyek

- Analisis data mahasiswa dengan pendekatan CRISP-DM
- Business dashboard interaktif berbasis Streamlit untuk monitoring performa mahasiswa
- Model ML prediksi dropout binary: **Dropout vs Graduate**
- Deployment prototype ke Streamlit Community Cloud

### Persiapan

**Sumber data:** [students_performance](https://github.com/dicodingacademy/dicoding_dataset/blob/main/students_performance/README.md)

**Setup environment:**

```bash
# Python yang digunakan: Python 3.11
# 1. Buat virtual environment
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
# venv\Scripts\activate        # Windows

# 2. Install semua dependencies
pip install -r requirements.txt
```

**Menjalankan Notebook:**
```bash
# Buka di VS Code
code notebook.ipynb

# Pilih kernel → venv → Run All
# Model tersimpan otomatis di folder model/
```

---

## Business Dashboard

Dashboard monitoring performa mahasiswa dibangun menggunakan **Streamlit** dengan 14 visualisasi interaktif yang dirancang untuk membantu pengambilan keputusan berbasis data.

**Menjalankan Dashboard (lokal):**
```bash
streamlit run dashboard.py
```

**Dashboard online:**
> 🔗 **https://project-students-performance-dashboard.streamlit.app/**

### Fitur & Visualisasi Dashboard

Dashboard dilengkapi **filter interaktif** di sidebar (Status, Gender, Penerima Beasiswa) yang memungkinkan stakeholder mengeksplorasi data secara dinamis.

| # | Visualisasi | Tujuan |
|---|-------------|--------|
| 1 | **KPI Overview** (6 kartu metrik) | Memberikan gambaran seketika: total mahasiswa, dropout rate, graduate rate, enrolled, dan rata-rata nilai Sem 1 & 2 |
| 2 | **Distribusi Status Siswa** (donut chart) | Memperlihatkan proporsi Dropout/Enrolled/Graduate secara visual untuk memahami skala masalah |
| 3 | **Dropout Rate per Program Studi** (bar horizontal) | Mengidentifikasi program studi dengan dropout tertinggi sebagai prioritas evaluasi kurikulum |
| 4 | **Distribusi Nilai Semester 1 & 2** (box plot) | Membandingkan distribusi nilai antar kelompok status untuk mengidentifikasi pola performa akademik |
| 5 | **Rata-rata MK Lulus per Status** (grouped bar) | Menunjukkan perbedaan produktivitas akademik antara Dropout dan Graduate |
| 6 | **Faktor Keuangan** (stacked bar: SPP, Beasiswa, Hutang) | Mengungkap pengaruh kondisi finansial terhadap kemungkinan dropout |
| 7 | **Distribusi Usia & Nilai Masuk** (histogram & violin) | Memahami profil demografis mahasiswa berisiko berdasarkan usia dan nilai seleksi |
| 8 | **Gender & Jadwal Kehadiran** (stacked bar) | Menganalisis pola dropout berdasarkan gender dan waktu kuliah (pagi/malam) |
| 9 | **Feature Importance** (bar horizontal) | Menampilkan faktor-faktor yang paling berpengaruh terhadap prediksi dropout berdasarkan model Random Forest |
| 10 | **Critical Academic Warning** (KPI + stacked bar) | Menghitung jumlah mahasiswa dengan success rate < 50% yang memerlukan intervensi segera |
| 11 | **Tren Progression Akademik** (line chart) | Memvisualisasikan bagaimana proporsi status berubah seiring meningkatnya jumlah MK yang lulus |
| 12 | **Demografi: Usia & Marital Status** (stacked bar) | Menganalisis pengaruh kelompok usia dan status pernikahan terhadap outcome mahasiswa |
| 13 | **Dropout Rate per Nationality** (bar horizontal) | Mengidentifikasi apakah mahasiswa dari negara tertentu memiliki risiko dropout di atas rata-rata |

---

## Menjalankan Prototype Machine Learning

**Lokal:**
```bash
streamlit run app.py
```

**Online (Streamlit Community Cloud):**
> 🔗 **https://project-students-performance-prediction.streamlit.app/**

Masukkan data akademik dan demografis mahasiswa, lalu klik **Prediksi**.
Hasil: **Dropout** atau **Graduate** beserta probabilitas dan faktor risiko yang teridentifikasi.

---

## Conclusion

### 1. Faktor-faktor Penyebab Dropout (EDA & Dashboard)

| # | Faktor | Temuan |
|---|--------|--------|
| 1 | **Nilai Semester 1 & 2** | Dropout mendekati nilai 0, Graduate berkisar 12–14 |
| 2 | **MK Lulus Semester 1 & 2** | Dropout lulus 0–2 MK, Graduate lulus 5–6 MK |
| 3 | **Status SPP** | SPP belum lunas → ~70% dropout, hanya ~8% graduate |
| 4 | **Status Beasiswa** | Penerima beasiswa memiliki dropout rate lebih rendah |
| 5 | **Usia saat Mendaftar** | Usia 26–30 dan 41+ memiliki dropout rate tertinggi |
| 6 | **Status Hutang** | Mahasiswa berhutang memiliki risiko dropout lebih tinggi |
| 7 | **Gender** | Laki-laki dropout ~45%, perempuan ~25% |

### 2. Performa Model Machine Learning

Model binary classification **Dropout vs Graduate** — data Enrolled dikecualikan dari training karena belum memiliki label akhir.

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|:--------:|:---------:|:------:|:--------:|
| **Random Forest** ⭐ | **0.9091** | **0.8933** | 0.9661 | **0.9283** |
| Decision Tree | 0.8939 | 0.8875 | 0.9457 | 0.9157 |
| Logistic Regression | 0.9105 | 0.8903 | **0.9729** | 0.9297 |

**Random Forest dipilih** karena memiliki keseimbangan terbaik antara Accuracy (90.91%), Precision (89.33%), dan F1-Score (92.83%).

**Top 5 Feature Importance:**
1. `Sem2_approval_rate` — rasio MK lulus Semester 2
2. `Total_approved` — total MK lulus kedua semester
3. `Curricular_units_2nd_sem_approved` — jumlah MK lulus Sem 2
4. `Avg_grade` — nilai rata-rata kedua semester
5. `Curricular_units_2nd_sem_grade` — nilai rata-rata Semester 2

### Rekomendasi Action Items

1. **Bimbingan Akademik Dini** — Mahasiswa dengan nilai Sem 1 rendah atau MK lulus < 3 segera diberi pendampingan intensif
2. **Fleksibilitas Pembayaran SPP** — Skema cicilan bagi mahasiswa yang kesulitan keuangan
3. **Perluasan Program Beasiswa** — Terbukti menurunkan dropout rate secara signifikan
4. **Early Warning System** — Monitoring bulanan; prob dropout ≥ 60% → bimbingan khusus
5. **Program Mentoring** — Khusus mahasiswa baru usia lebih tua dan mahasiswa laki-laki

---

## Struktur Proyek

```
submission project/
├── model/
│   ├── model.joblib
│   ├── scaler.joblib
│   ├── label_encoder.joblib
│   └── feature_names.joblib
├── .streamlit/
│   └── config.toml
├── notebook.ipynb
├── app.py
├── dashboard.py
├── README.md
├── requirements.txt
├── data.csv
└── sutriadik24-dashboard.png
```